"""
Compliance Evaluation Node - Core evaluation logic.
Compares documentation against compliance rules and identifies violations.
"""

import json
from typing import List, Dict, Any, Optional
from langchain_groq import ChatGroq
from src.state import ComplianceState, Violation, ComplianceRule, DocumentBlock, SeverityLevel
from src.config import Config


class ComplianceEvaluationNode:
    """
    Core evaluation node that matches documentation against compliance rules.
    Uses Grok API to perform intelligent rule matching and violation detection.
    """
    
    def __init__(self):
        # Initialize Grok LLM
        llm_config = Config.get_llm_config()
        self.llm = ChatGroq(
            api_key=llm_config["api_key"],
            model=llm_config["model"],
            temperature=llm_config["temperature"],
            max_tokens=llm_config["max_tokens"]
        )
    
    def execute(self, state: ComplianceState) -> ComplianceState:
        """
        Main execution function for compliance evaluation.
        
        Args:
            state: Current compliance state
            
        Returns:
            Updated state with identified violations
        """
        try:
            state["processing_stage"] = "compliance_evaluation"
            
            if not state["documents"]:
                state["warnings"].append("No documents to evaluate")
                return state
            
            if not state["rules"]:
                state["warnings"].append("No rules loaded for evaluation")
                return state
            
            # Evaluate each rule against all documents
            all_violations = []
            preliminary_matches = {}
            
            for rule in state["rules"]:
                violations = self._evaluate_rule(rule, state["documents"])
                all_violations.extend(violations)
                preliminary_matches[rule["rule_id"]] = {
                    "violations_found": len(violations),
                    "rule_name": rule["name"]
                }
            
            state["violations"] = all_violations
            state["preliminary_matches"] = preliminary_matches
            
            if Config.VERBOSE:
                print(f"✓ Compliance evaluation complete: {len(all_violations)} violations found")
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Compliance evaluation error: {str(e)}")
            print(f"✗ Compliance evaluation failed: {str(e)}")
            return state
    
    def _evaluate_rule(self, rule: ComplianceRule, documents: List[DocumentBlock]) -> List[Violation]:
        """
        Evaluate a single rule against all documents.
        
        Args:
            rule: Compliance rule to evaluate
            documents: List of document blocks
            
        Returns:
            List of violations found
        """
        violations = []
        
        # Combine all document content with source tracking
        doc_content = self._prepare_document_context(documents)
        
        # Create evaluation prompt
        prompt = self._create_evaluation_prompt(rule, doc_content)
        
        # Query Grok for evaluation
        try:
            response = self.llm.invoke(prompt)
            result = self._parse_evaluation_response(response.content, rule)
            
            if result and result.get("violations"):
                for violation_data in result["violations"]:
                    violation: Violation = {
                        "rule_id": rule["rule_id"],
                        "rule_name": rule["name"],
                        "evidence": violation_data.get("evidence", "No evidence provided"),
                        "severity": rule["severity"],
                        "explanation": violation_data.get("explanation", ""),
                        "location": violation_data.get("location"),
                        "confidence": violation_data.get("confidence", 0.8)
                    }
                    violations.append(violation)
        
        except Exception as e:
            print(f"Warning: Error evaluating rule {rule['rule_id']}: {str(e)}")
        
        return violations
    
    def _prepare_document_context(self, documents: List[DocumentBlock]) -> str:
        """
        Prepare document content for evaluation.
        
        Args:
            documents: List of document blocks
            
        Returns:
            Formatted document context
        """
        context_parts = []
        
        for i, doc in enumerate(documents):
            context_parts.append(f"--- Document {i+1}: {doc['metadata']['file_name']} ({doc['doc_type']}) ---")
            context_parts.append(doc["content"])
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def _create_evaluation_prompt(self, rule: ComplianceRule, doc_content: str) -> str:
        """
        Create a prompt for the LLM to evaluate compliance.
        
        Args:
            rule: Compliance rule to evaluate
            doc_content: Document content to check
            
        Returns:
            Formatted prompt
        """
        examples_text = ""
        if rule.get("examples"):
            examples_text = "\n\nExamples of violations:\n" + "\n".join(f"- {ex}" for ex in rule["examples"])
        
        prompt = f"""You are a compliance auditor. Evaluate the following documents against this compliance rule:

RULE ID: {rule['rule_id']}
RULE NAME: {rule['name']}
DESCRIPTION: {rule['description']}
CATEGORY: {rule['category']}
SEVERITY: {rule['severity']}
CRITERIA: {rule['criteria']}{examples_text}

DOCUMENTS TO EVALUATE:
{doc_content}

TASK:
Carefully analyze the documents to determine if they violate this compliance rule.
For each violation found, identify:
1. The specific evidence (quote the relevant text)
2. The location (file/section)
3. A clear explanation of why it violates the rule
4. Your confidence level (0.0 to 1.0)

Respond ONLY with a valid JSON object in this exact format:
{{
  "compliant": true/false,
  "violations": [
    {{
      "evidence": "quoted text showing the violation",
      "location": "file name or section",
      "explanation": "why this violates the rule",
      "confidence": 0.85
    }}
  ],
  "notes": "any additional observations"
}}

If no violations found, return: {{"compliant": true, "violations": [], "notes": "Rule satisfied"}}
"""
        return prompt
    
    def _parse_evaluation_response(self, response: str, rule: ComplianceRule) -> Optional[Dict[str, Any]]:
        """
        Parse the LLM response into structured data.
        
        Args:
            response: LLM response text
            rule: The rule being evaluated
            
        Returns:
            Parsed response dictionary or None
        """
        try:
            # Try to extract JSON from response
            response = response.strip()
            
            # Handle markdown code blocks
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join(lines[1:-1]) if len(lines) > 2 else response
                response = response.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(response)
            return result
            
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse response for rule {rule['rule_id']}: {str(e)}")
            return None


def compliance_evaluation_node(state: ComplianceState) -> ComplianceState:
    """
    LangGraph node function for compliance evaluation.
    
    Args:
        state: Current compliance state
        
    Returns:
        Updated state with violations
    """
    node = ComplianceEvaluationNode()
    return node.execute(state)