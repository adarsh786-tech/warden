"""
State schema for the Compliance Audit Agent workflow.
Defines the structured data passed between LangGraph nodes.
"""

from typing import TypedDict, List, Dict, Optional, Any
from enum import Enum


class SeverityLevel(str, Enum):
    """Enumeration for violation severity levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Violation(TypedDict):
    """Structure for a single compliance violation."""
    rule_id: str
    rule_name: str
    evidence: str  # Text snippet showing the violation
    severity: SeverityLevel
    explanation: str  # Why this is a violation
    location: Optional[str]  # File/section where found
    confidence: float  # 0.0 to 1.0


class ComplianceRule(TypedDict):
    """Structure for a compliance rule definition."""
    rule_id: str
    name: str
    description: str
    category: str  # e.g., "security", "documentation", "data-privacy"
    severity: SeverityLevel
    criteria: str  # What to check for
    examples: Optional[List[str]]


class DocumentBlock(TypedDict):
    """Structure for processed document content."""
    source: str  # File name or document identifier
    content: str
    doc_type: str  # e.g., "readme", "policy", "code", "config"
    metadata: Dict[str, Any]


class RiskScore(TypedDict):
    """Risk assessment breakdown."""
    high_count: int
    medium_count: int
    low_count: int
    total_issues: int
    compliance_percentage: float
    overall_risk: str  # "critical", "high", "moderate", "low"


class ReflectionNote(TypedDict):
    """Notes from the reflection and reasoning loop."""
    iteration: int
    original_finding: str
    reassessment: str
    confidence_before: float
    confidence_after: float
    action_taken: str  # "confirmed", "revised", "removed"


class AuditReport(TypedDict):
    """Final structured audit report."""
    timestamp: str
    compliance_score: float
    risk_assessment: RiskScore
    violations: List[Violation]
    missing_artifacts: List[str]
    recommendations: List[str]
    summary: str
    traceable_evidence: Dict[str, Any]


class ComplianceState(TypedDict):
    """
    Main state object passed between LangGraph nodes.
    This represents the complete session state for the audit workflow.
    """
    
    # Input data
    documents: List[DocumentBlock]
    raw_input_paths: List[str]
    
    # Compliance rules
    rules: List[ComplianceRule]
    active_rule_categories: List[str]
    
    # Analysis results
    violations: List[Violation]
    preliminary_matches: Dict[str, Any]
    
    # Risk scoring
    risk_scores: Optional[RiskScore]
    severity_breakdown: Dict[str, int]
    
    # Reflection loop data
    reflection_enabled: bool
    reflection_notes: List[ReflectionNote]
    needs_refinement: bool
    current_iteration: int
    
    # Final outputs
    final_report: Optional[AuditReport]
    audit_passed: bool
    
    # Metadata and tracking
    processing_stage: str  # Current node being executed
    errors: List[str]
    warnings: List[str]
    execution_metadata: Dict[str, Any]


def create_initial_state() -> ComplianceState:
    """Factory function to create a new initial state."""
    return ComplianceState(
        documents=[],
        raw_input_paths=[],
        rules=[],
        active_rule_categories=[],
        violations=[],
        preliminary_matches={},
        risk_scores=None,
        severity_breakdown={},
        reflection_enabled=True,
        reflection_notes=[],
        needs_refinement=False,
        current_iteration=0,
        final_report=None,
        audit_passed=False,
        processing_stage="initialized",
        errors=[],
        warnings=[],
        execution_metadata={}
    )