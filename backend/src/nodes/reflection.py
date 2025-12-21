"""
Reflection & Reasoning Loop Node - Re-evaluates ambiguous findings.
Performs self-checking to validate decisions and reduce false positives.
"""

import json
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from src.state import ComplianceState, Violation, ReflectionNote
from src.config import Config


class ReflectionNode:
    """
    Reflection node that re-evaluates uncertain or ambiguous violations.
    Uses iterative reasoning to improve confidence and reduce false positives.
    """
    
    def __init__(self):
        # Initialize Grok LLM
        llm_config = Config.get_llm_config()
        self.llm = ChatGroq(
            api_key=llm_config["api_key"],
            base_url=llm_config["base_url"],
            model=llm_config["model"],
            temperature=llm_config["temperature"],
            max_tokens=llm_config["max_tokens"]
        )
    
    def execute(self, state: ComplianceState) -> ComplianceState:
        """
        Main execution function for reflection.
        
        Args:
            state: Current compliance state
            
        Returns:
            Updated state with refined violations
        """
        try:
            state["processing_stage"] = "reflection"
            
            # Skip reflection if disabled
            if not Config.ENABLE_REFLECTION or not state.get("reflection_enabled", True):
                if Config.VERBOSE:
                    print("⊘ Reflection disabled, skipping")
                return state
            
            # Check iteration limit
            if state["current_iteration"] >= Config.MAX_REFLECTION_ITERATIONS:
                if Config.VERBOSE:
                    print(f"⊘ Maximum reflection iterations ({Config.MAX_REFLECTION_ITERATIONS}) reached")
                return state
            
            # Identify violations that need reflection
            violations_to_reflect = self._identify_uncertain_violations(state["violations"])
            
            if not violations_to_reflect:
                if Config.VERBOSE:
                    print("✓ No uncertain violations, reflection not needed")
                return state
            
            # Perform reflection on uncertain violations
            reflection_notes = []
            refined_violations = []
            
            for violation in state["violations"]:
                if violation in violations_to_reflect:
                    reflected_result = self._reflect_on_violation(violation, state)
                    reflection_notes.append(reflected_result["note"])
                    
                    # Keep or remove violation based on reflection
                    if reflected_result["keep_violation"]:
                        # Update violation with refined confidence
                        violation["confidence"] = reflected_result["new_confidence"]
                        violation["explanation"] = reflected_result.get("refined_explanation", violation["explanation"])
                        refined_violations.append(violation)
                else:
                    # Keep violations that don't need reflection
                    refined_violations.append(violation)
            
            # Update state
            state["violations"] = refined_violations
            state["reflection_notes"].extend(reflection_notes)
            state["current_iteration"] += 1
            
            # Check if further refinement is needed
            state["needs_refinement"] = any(
                v["confidence"] < Config.CONFIDENCE_THRESHOLD 
                for v in refined_violations
            )
            
            if Config.VERBOSE:
                print(f"✓ Reflection complete (iteration {state['current_iteration']}):")
                print(f"  Reflected on {len(violations_to_reflect)} violations")
                print(f"  Retained {len(refined_violations)} violations")
                print(f"  Removed {len(state['violations']) - len(refined_violations)} false positives")
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Reflection error: {str(e)}")
            print(f"✗ Reflection failed: {str(e)}")
            return state
    
    def _identify_uncertain_violations(self, violations: List[Violation]) -> List[Violation]:
        """
        Identify violations with low confidence that need reflection.
        
        Args:
            violations: List of all violations
            
        Returns:
            List of violations needing reflection
        """
        uncertain = [
            v for v in violations 
            if v.get("confidence", 1.0) < Config.CONFIDENCE_THRESHOLD
        ]
        
        return uncertain
    
    def _reflect_on_violation(self, violation: Violation, state: ComplianceState) -> Dict[str, Any]:
        """
        Perform reflection on a single violation.
        
        Args:
            violation: Violation to reflect upon
            state: Current compliance state
            
        Returns:
            Reflection result with decision
        """
        # Get the original rule
        rule = next((r for r in state["rules"] if r["rule_id"] == violation["rule_id"]), None)
        
        if not rule:
            # Cannot reflect without rule context
            return {
                "note": self._create_reflection_note(violation, "no_rule", 0, 0, "confirmed"),
                "keep_violation": True,
                "new_confidence": violation["confidence"]
            }
        
        # Create reflection prompt
        prompt = self._create_reflection_prompt(violation, rule, state)
        
        # Query Grok for reflection
        try:
            response = self.llm.invoke(prompt)
            result = self._parse_reflection_response(response.content)
            
            if result:
                keep = result.get("is_valid_violation", True)
                new_confidence = result.get("confidence", violation["confidence"])
                action = "confirmed" if keep else "removed"
                
                note = self._create_reflection_note(
                    violation,
                    result.get("reasoning", ""),
                    violation["confidence"],
                    new_confidence,
                    action
                )
                
                return {
                    "note": note,
                    "keep_violation": keep,
                    "new_confidence": new_confidence,
                    "refined_explanation": result.get("refined_explanation", violation["explanation"])
                }
        
        except Exception as e:
            print(f"Warning: Reflection failed for {violation['rule_id']}: {str(e)}")
        
        # Default: keep violation with original confidence
        return {
            "note": self._create_reflection_note(violation, "reflection_failed", 0, 0, "confirmed"),
            "keep_violation": True,
            "new_confidence": violation["confidence"]
        }
    
    def _create_reflection_prompt(self, violation: Violation, rule: Dict, state: ComplianceState) -> str:
        """
        Create a reflection prompt for re-evaluation.
        
        Args:
            violation: Violation to reflect on
            rule: Associated compliance rule
            state: Current state for context
            
        Returns:
            Reflection prompt
        """
        prompt = f"""You are performing a reflection and quality check on a compliance violation finding.

ORIGINAL FINDING:
Rule ID: {violation['rule_id']}
Rule Name: {violation['rule_name']}
Evidence: {violation['evidence']}
Explanation: {violation['explanation']}
Location: {violation.get('location', 'Not specified')}
Current Confidence: {violation['confidence']}

RULE DETAILS:
Description: {rule['description']}
Criteria: {rule['criteria']}
Severity: {rule['severity']}

TASK:
Re-evaluate this finding with fresh eyes. Consider:
1. Is the evidence truly a violation of this rule?
2. Could this be a false positive or misinterpretation?
3. Is there important context that was missed?
4. How confident should we be in this finding?

Respond ONLY with valid JSON in this format:
{{
  "is_valid_violation": true/false,
  "confidence": 0.0-1.0,
  "reasoning": "detailed explanation of your reflection",
  "refined_explanation": "improved explanation if violation is valid",
  "recommendation": "keep, revise, or remove"
}}
"""
        return prompt
    
    def _parse_reflection_response(self, response: str) -> Dict[str, Any]:
        """
        Parse reflection response from LLM.
        
        Args:
            response: LLM response text
            
        Returns:
            Parsed reflection result
        """
        try:
            response = response.strip()
            
            # Handle markdown code blocks
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join(lines[1:-1]) if len(lines) > 2 else response
                response = response.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(response)
            return result
            
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse reflection response: {str(e)}")
            return None
    
    def _create_reflection_note(
        self,
        violation: Violation,
        reasoning: str,
        confidence_before: float,
        confidence_after: float,
        action: str
    ) -> ReflectionNote:
        """
        Create a reflection note for tracking.
        
        Args:
            violation: Violation that was reflected upon
            reasoning: Reasoning for the decision
            confidence_before: Original confidence
            confidence_after: Updated confidence
            action: Action taken
            
        Returns:
            Reflection note
        """
        note: ReflectionNote = {
            "iteration": 0,  # Will be set by state
            "original_finding": f"{violation['rule_id']}: {violation['rule_name']}",
            "reassessment": reasoning,
            "confidence_before": confidence_before,
            "confidence_after": confidence_after,
            "action_taken": action
        }
        
        return note


def reflection_node(state: ComplianceState) -> ComplianceState:
    """
    LangGraph node function for reflection.
    
    Args:
        state: Current compliance state
        
    Returns:
        Updated state with refined violations
    """
    node = ReflectionNode()
    return node.execute(state)