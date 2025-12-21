"""
LangGraph Workflow Definition - Connects all nodes into a workflow.
Defines the compliance audit agent graph with conditional routing.
"""

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
        Execute workflow for API usage - returns JSON-serializable result.
        
        Args:
            file_paths: List of uploaded file paths
            
        Returns:
            Dictionary containing audit results
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
            
            # Extract key results
            result = {
                "success": len(final_state.get("errors", [])) == 0,
                "audit_passed": final_state.get("audit_passed", False),
                "errors": final_state.get("errors", []),
                "warnings": final_state.get("warnings", [])
            }
            
            # Add report if available
            if final_state.get("final_report"):
                report = final_state["final_report"]
                result["report"] = {
                    "timestamp": report.get("timestamp"),
                    "compliance_score": report.get("compliance_score"),
                    "risk_assessment": self._serialize_risk_assessment(report.get("risk_assessment")),
                    "violations": self._serialize_violations(report.get("violations", [])),
                    "missing_artifacts": report.get("missing_artifacts", []),
                    "recommendations": report.get("recommendations", []),
                    "summary": report.get("summary")
                }
            
            return result
            
        finally:
            Config.VERBOSE = original_verbose
    
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