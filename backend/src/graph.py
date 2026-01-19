"""
LangGraph Workflow Definition - Connects all nodes into a workflow.
Defines the compliance audit agent graph with conditional routing.
"""
import os
from datetime import datetime
from langgraph.graph import StateGraph, END
from src.state import ComplianceState, create_initial_state
from src.nodes import (
    ingestion_node,
    rule_retrieval_node,
    compliance_evaluation_node,
    risk_classification_node,
    reflection_node,
    report_generation_node,
    output_dispatcher_node
)
from src.config import Config


class ComplianceAuditGraph:
    """
    Main workflow graph for the compliance audit agent.
    Orchestrates the multi-agent reasoning process.
    """
    
    def __init__(self):
        self.graph = self._build_graph()
        self.compiled_graph = None
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow.
        
        Returns:
            Configured StateGraph
        """
        # Initialize the graph with our state schema
        workflow = StateGraph(ComplianceState)
        
        # Add all nodes
        workflow.add_node("ingestion", ingestion_node)
        workflow.add_node("rule_retrieval", rule_retrieval_node)
        workflow.add_node("compliance_evaluation", compliance_evaluation_node)
        workflow.add_node("risk_classification", risk_classification_node)
        workflow.add_node("reflection", reflection_node)
        workflow.add_node("report_generation", report_generation_node)
        workflow.add_node("output_dispatcher", output_dispatcher_node)
        
        # Define the workflow edges
        # Linear flow: ingestion -> rules -> evaluation -> risk -> reflection -> report -> output
        workflow.set_entry_point("ingestion")
        workflow.add_edge("ingestion", "rule_retrieval")
        workflow.add_edge("rule_retrieval", "compliance_evaluation")
        workflow.add_edge("compliance_evaluation", "risk_classification")
        
        # Conditional edge for reflection loop
        workflow.add_conditional_edges(
            "risk_classification",
            self._should_reflect,
            {
                "reflect": "reflection",
                "skip": "report_generation"
            }
        )
        
        # Conditional edge for iterative reflection
        workflow.add_conditional_edges(
            "reflection",
            self._needs_more_reflection,
            {
                "continue": "risk_classification",  # Re-score after reflection
                "done": "report_generation"
            }
        )
        
        workflow.add_edge("report_generation", "output_dispatcher")
        workflow.add_edge("output_dispatcher", END)
        
        return workflow
    
    def _should_reflect(self, state: ComplianceState) -> str:
        """
        Determine if reflection should be performed.
        
        Args:
            state: Current compliance state
            
        Returns:
            "reflect" or "skip"
        """
        # Skip if reflection is disabled
        if not Config.ENABLE_REFLECTION or not state.get("reflection_enabled", True):
            return "skip"
        
        # Skip if no violations to reflect on
        if not state.get("violations"):
            return "skip"
        
        # Skip if max iterations reached
        if state["current_iteration"] >= Config.MAX_REFLECTION_ITERATIONS:
            return "skip"
        
        # Check if any violations have low confidence
        violations = state.get("violations", [])
        uncertain_violations = [
            v for v in violations 
            if v.get("confidence", 1.0) < Config.CONFIDENCE_THRESHOLD
        ]
        
        if uncertain_violations:
            return "reflect"
        
        return "skip"
    
    def _needs_more_reflection(self, state: ComplianceState) -> str:
        """
        Determine if more reflection iterations are needed.
        
        Args:
            state: Current compliance state
            
        Returns:
            "continue" or "done"
        """
        # Check if we've reached max iterations
        if state["current_iteration"] >= Config.MAX_REFLECTION_ITERATIONS:
            return "done"
        
        # Check if refinement is still needed
        if state.get("needs_refinement", False):
            # Check if there are still uncertain violations
            violations = state.get("violations", [])
            uncertain = [
                v for v in violations 
                if v.get("confidence", 1.0) < Config.CONFIDENCE_THRESHOLD
            ]
            
            if uncertain:
                return "continue"
        
        return "done"
    
    def compile(self):
        """
        Compile the graph for execution.
        
        Returns:
            Compiled graph
        """
        if not self.compiled_graph:
            self.compiled_graph = self.graph.compile()
        
        return self.compiled_graph
    
    def visualize(self, output_path: str = "workflow_diagram.png"):
        """
        Visualize the workflow graph (requires graphviz).
        
        Args:
            output_path: Path to save the visualization
        """
        try:
            from IPython.display import Image, display
            
            compiled = self.compile()
            graph_image = compiled.get_graph().draw_mermaid_png()
            
            with open(output_path, "wb") as f:
                f.write(graph_image)
            
            print(f"Workflow diagram saved to: {output_path}")
            
        except ImportError:
            print("Visualization requires IPython and graphviz")
        except Exception as e:
            print(f"Could not visualize graph: {str(e)}")
    
    def run(self, initial_state: ComplianceState = None, custom_paths: list = None) -> ComplianceState:
        """
        Execute the complete workflow.
        
        Args:
            initial_state: Optional initial state (creates new if None)
            custom_paths: Optional list of file paths to audit (for API usage)
            
        Returns:
            Final state after workflow completion
        """
        if initial_state is None:
            initial_state = create_initial_state()
        
        # If custom paths provided (from API), override default paths
        if custom_paths:
            initial_state["raw_input_paths"] = custom_paths
        
        compiled = self.compile()
        
        if Config.VERBOSE:
            print("\n" + "="*80)
            print("STARTING COMPLIANCE AUDIT WORKFLOW")
            print("="*80 + "\n")
        
        # Execute the workflow
        final_state = compiled.invoke(initial_state)
        
        if Config.VERBOSE:
            print("\n" + "="*80)
            print("WORKFLOW EXECUTION COMPLETE")
            print("="*80 + "\n")
        
        return final_state
    
    def run_api(self, file_paths: list) -> dict:
        """
        Execute workflow for API usage - returns JSON-serializable result matching frontend format.
        
        Args:
            file_paths: List of uploaded file paths
            
        Returns:
            Dictionary containing audit results in frontend-compatible format
        """
        # Create initial state
        initial_state = create_initial_state()
        initial_state["raw_input_paths"] = file_paths
        
        # Run workflow without verbose output
        original_verbose = Config.VERBOSE
        Config.VERBOSE = False
        
        try:
            compiled = self.compile()
            final_state = compiled.invoke(initial_state)
            
            # Get report data
            report = final_state.get("final_report")
            risk_assessment = report.get("risk_assessment") if report else None
            violations = report.get("violations", []) if report else []
            
            # Transform to frontend format
            result = {
                "success": len(final_state.get("errors", [])) == 0,
                "status": "completed",
                "auditPassed": final_state.get("audit_passed", False),
                "complianceScore": report.get("compliance_score", 0) if report else 0,
                "criticalIssues": risk_assessment.get("high_count", 0) if risk_assessment else 0,
                "moderateIssues": risk_assessment.get("medium_count", 0) if risk_assessment else 0,
                "lowIssues": risk_assessment.get("low_count", 0) if risk_assessment else 0,
                "totalViolations": risk_assessment.get("total_issues", 0) if risk_assessment else 0,
                "riskLevel": self._map_risk_level(risk_assessment.get("overall_risk", "unknown") if risk_assessment else "unknown"),
                "missingArtifacts": len(report.get("missing_artifacts", [])) if report else 0,
                "missingArtifactsList": report.get("missing_artifacts", []) if report else [],
                "violations": self._serialize_violations_for_frontend(violations),
                "recommendations": report.get("recommendations", []) if report else [],
                "summary": report.get("summary", "") if report else "",
                "auditInfo": {
                    "status": "completed",
                    "lastRun": report.get("timestamp") if report else datetime.now().isoformat(),
                    "duration": self._calculate_duration(final_state),
                    "rulesEvaluated": len(final_state.get("rules", [])),
                    "artifactsScanned": len(final_state.get("documents", [])),
                    "documentsAnalyzed": len(final_state.get("documents", [])),
                },
                "metadata": {
                    "timestamp": report.get("timestamp") if report else datetime.now().isoformat(),
                    "filesAnalyzed": len(file_paths),
                    "fileNames": [os.path.basename(p) for p in file_paths],
                },
                "errors": final_state.get("errors", []),
                "warnings": final_state.get("warnings", [])
            }
            
            return result
            
        finally:
            Config.VERBOSE = original_verbose
    
    def _map_risk_level(self, backend_risk: str) -> str:
        """Map backend risk levels to frontend expected values."""
        risk_mapping = {
            "critical": "critical",
            "high": "high",
            "moderate": "medium",
            "low": "low",
            "unknown": "low"
        }
        return risk_mapping.get(backend_risk, "low")

    def _calculate_duration(self, state: ComplianceState) -> str:
        """Calculate a human-readable duration string."""
        # This is a simplified version - you could track actual start/end times
        doc_count = len(state.get("documents", []))
        rule_count = len(state.get("rules", []))
        
        # Rough estimate: 1s per document + 0.5s per rule
        estimated_seconds = doc_count * 1 + rule_count * 0.5
        
        if estimated_seconds < 60:
            return f"{int(estimated_seconds)}s"
        else:
            minutes = int(estimated_seconds // 60)
            seconds = int(estimated_seconds % 60)
            return f"{minutes}m {seconds}s"

    def _serialize_violations_for_frontend(self, violations):
        """Convert violations to frontend-compatible format with detailed information."""
        serialized = []
        
        for i, v in enumerate(violations):
            # Generate unique ID
            violation_id = f"v-{str(i+1).zfill(3)}"
            
            # Map severity
            severity_map = {
                "high": "critical",
                "medium": "high",
                "low": "medium"
            }
            frontend_severity = severity_map.get(
                v.get("severity").value if hasattr(v.get("severity"), "value") else v.get("severity"),
                "medium"
            )
            
            # Determine category from rule_id
            category = self._determine_category(v.get("rule_id", ""))
            
            # Build violation object matching frontend structure
            violation_obj = {
                "id": violation_id,
                "ruleId": v.get("rule_id"),
                "title": v.get("rule_name"),
                "description": v.get("explanation", "No description provided"),
                "severity": frontend_severity,
                "status": "open",  # Default status
                "category": category,
                "evidence": v.get("evidence", "No evidence provided"),
                "reasoning": v.get("explanation", ""),
                "remediation": self._generate_remediation(v),
                "confidence": int(v.get("confidence", 0.8) * 100),  # Convert to percentage
                "detectedAt": datetime.now().isoformat(),
                "location": v.get("location", "Not specified")
            }
            
            # Add reflection if available (from reflection notes)
            if v.get("reflection_note"):
                violation_obj["reflection"] = {
                    "initialFinding": v.get("reflection_note", {}).get("original_finding", ""),
                    "reflectionNotes": v.get("reflection_note", {}).get("reassessment", ""),
                    "finalDecision": v.get("reflection_note", {}).get("action_taken", "confirmed")
                }
            
            serialized.append(violation_obj)
        
        return serialized

    def _determine_category(self, rule_id: str) -> str:
        """Determine violation category from rule ID."""
        if rule_id.startswith("SEC"):
            return "Security"
        elif rule_id.startswith("DOC"):
            return "Documentation"
        elif rule_id.startswith("PRIV"):
            return "Privacy"
        elif rule_id.startswith("AUTH"):
            return "Authentication"
        elif rule_id.startswith("LOG"):
            return "Audit Logging"
        elif rule_id.startswith("ACC"):
            return "Access Control"
        elif rule_id.startswith("DEP"):
            return "Dependencies"
        else:
            return "General"

    def _generate_remediation(self, violation: dict) -> str:
        """Generate remediation steps for a violation."""
        rule_id = violation.get("rule_id", "")
        
        # Default remediation templates
        remediation_templates = {
            "SEC-001": "1. Implement password hashing using bcrypt or argon2\n2. Update password storage logic\n3. Audit existing passwords and force reset\n4. Add password strength requirements",
            "SEC-002": "1. Move API keys to environment variables\n2. Use a secrets management service (e.g., AWS Secrets Manager, HashiCorp Vault)\n3. Rotate exposed keys immediately\n4. Add pre-commit hooks to prevent future exposure",
            "SEC-003": "1. Implement input validation for all user inputs\n2. Use parameterized queries for database operations\n3. Add sanitization middleware\n4. Conduct security review of all input handlers",
            "SEC-004": "1. Enable logging for authentication events\n2. Implement structured logging with appropriate detail levels\n3. Set up log aggregation and monitoring\n4. Define log retention policies",
            "SEC-005": "1. Enforce HTTPS for all connections\n2. Update configuration to redirect HTTP to HTTPS\n3. Implement HSTS headers\n4. Review all network communication paths",
            "DOC-001": "1. Create README.md with project overview\n2. Include setup and installation instructions\n3. Document configuration options\n4. Add usage examples and troubleshooting guide",
            "DOC-002": "1. Create SECURITY.md file\n2. Document security policies and procedures\n3. Include incident response plan\n4. Add contact information for security issues",
            "DOC-003": "1. Create dependency manifest (requirements.txt, package.json, etc.)\n2. Document all dependencies with versions\n3. Set up dependency scanning\n4. Establish update procedures",
            "PRIV-001": "1. Document PII collection practices\n2. Create data handling procedures\n3. Implement data classification\n4. Add privacy policy",
            "PRIV-002": "1. Define data retention periods\n2. Implement automated data deletion\n3. Document retention policy\n4. Add user data export functionality"
        }
        
        return remediation_templates.get(rule_id, 
            f"1. Review and address the violation described above\n2. Update relevant code or documentation\n3. Verify compliance with {rule_id}\n4. Document changes made")

    def _serialize_risk_assessment(self, risk_assessment):
        """Convert risk assessment to JSON-serializable format."""
        if not risk_assessment:
            return None
        
        return {
            "high_count": risk_assessment.get("high_count", 0),
            "medium_count": risk_assessment.get("medium_count", 0),
            "low_count": risk_assessment.get("low_count", 0),
            "total_issues": risk_assessment.get("total_issues", 0),
            "compliance_percentage": risk_assessment.get("compliance_percentage", 0.0),
            "overall_risk": risk_assessment.get("overall_risk", "unknown")
        }
    
    def _serialize_violations(self, violations):
        """Convert violations to JSON-serializable format."""
        serialized = []
        for v in violations:
            serialized.append({
                "rule_id": v.get("rule_id"),
                "rule_name": v.get("rule_name"),
                "evidence": v.get("evidence"),
                "severity": v.get("severity").value if hasattr(v.get("severity"), "value") else v.get("severity"),
                "explanation": v.get("explanation"),
                "location": v.get("location"),
                "confidence": v.get("confidence")
            })
        return serialized
    
    def stream(self, initial_state: ComplianceState = None):
        """
        Stream the workflow execution with intermediate states.
        
        Args:
            initial_state: Optional initial state
            
        Yields:
            State at each step of execution
        """
        if initial_state is None:
            initial_state = create_initial_state()
        
        compiled = self.compile()
        
        if Config.VERBOSE:
            print("\n" + "="*80)
            print("STREAMING COMPLIANCE AUDIT WORKFLOW")
            print("="*80 + "\n")
        
        for state in compiled.stream(initial_state):
            yield state
        
        if Config.VERBOSE:
            print("\n" + "="*80)
            print("WORKFLOW STREAM COMPLETE")
            print("="*80 + "\n")


def create_compliance_audit_graph() -> ComplianceAuditGraph:
    """
    Factory function to create a new compliance audit graph.
    
    Returns:
        Configured ComplianceAuditGraph
    """
    return ComplianceAuditGraph()