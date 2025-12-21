"""
Risk Classification Node - Assigns severity scores and risk levels.
Analyzes violations and calculates overall compliance metrics.
"""

from typing import Dict, List
from src.state import ComplianceState, RiskScore, SeverityLevel, Violation
from src.config import Config


class RiskClassificationNode:
    """
    Classifies and scores the risk level based on identified violations.
    Calculates compliance percentage and overall risk assessment.
    """
    
    def __init__(self):
        # Weight factors for different severity levels
        self.severity_weights = {
            SeverityLevel.HIGH: 3.0,
            SeverityLevel.MEDIUM: 2.0,
            SeverityLevel.LOW: 1.0
        }
    
    def execute(self, state: ComplianceState) -> ComplianceState:
        """
        Main execution function for risk classification.
        
        Args:
            state: Current compliance state
            
        Returns:
            Updated state with risk scores and classification
        """
        try:
            state["processing_stage"] = "risk_classification"
            
            violations = state["violations"]
            rules = state["rules"]
            
            # Calculate severity breakdown
            severity_breakdown = self._calculate_severity_breakdown(violations)
            state["severity_breakdown"] = severity_breakdown
            
            # Calculate compliance percentage
            compliance_score = self._calculate_compliance_score(
                violations, rules, severity_breakdown
            )
            
            # Determine overall risk level
            overall_risk = self._determine_overall_risk(severity_breakdown, compliance_score)
            
            # Create risk score object
            risk_score: RiskScore = {
                "high_count": severity_breakdown.get("high", 0),
                "medium_count": severity_breakdown.get("medium", 0),
                "low_count": severity_breakdown.get("low", 0),
                "total_issues": len(violations),
                "compliance_percentage": compliance_score,
                "overall_risk": overall_risk
            }
            
            state["risk_scores"] = risk_score
            
            # Determine if audit passed based on thresholds
            state["audit_passed"] = self._determine_audit_result(risk_score)
            
            if Config.VERBOSE:
                print(f"✓ Risk classification complete:")
                print(f"  Compliance Score: {compliance_score:.1f}%")
                print(f"  Overall Risk: {overall_risk}")
                print(f"  Critical Issues: {risk_score['high_count']}")
                print(f"  Moderate Issues: {risk_score['medium_count']}")
                print(f"  Low Issues: {risk_score['low_count']}")
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Risk classification error: {str(e)}")
            print(f"✗ Risk classification failed: {str(e)}")
            return state
    
    def _calculate_severity_breakdown(self, violations: List[Violation]) -> Dict[str, int]:
        """
        Calculate count of violations by severity level.
        
        Args:
            violations: List of violations
            
        Returns:
            Dictionary with counts by severity
        """
        breakdown = {
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for violation in violations:
            severity = violation["severity"].value
            breakdown[severity] = breakdown.get(severity, 0) + 1
        
        return breakdown
    
    def _calculate_compliance_score(
        self, 
        violations: List[Violation], 
        rules: List,
        severity_breakdown: Dict[str, int]
    ) -> float:
        """
        Calculate overall compliance percentage.
        
        Uses weighted scoring where high severity violations have more impact.
        
        Args:
            violations: List of violations
            rules: List of compliance rules
            severity_breakdown: Breakdown by severity
            
        Returns:
            Compliance percentage (0-100)
        """
        if not rules:
            return 100.0
        
        # Calculate weighted violation score
        weighted_violations = (
            severity_breakdown.get("high", 0) * self.severity_weights[SeverityLevel.HIGH] +
            severity_breakdown.get("medium", 0) * self.severity_weights[SeverityLevel.MEDIUM] +
            severity_breakdown.get("low", 0) * self.severity_weights[SeverityLevel.LOW]
        )
        
        # Calculate maximum possible weighted score
        max_weighted_score = len(rules) * self.severity_weights[SeverityLevel.HIGH]
        
        # Calculate compliance percentage
        if max_weighted_score == 0:
            return 100.0
        
        compliance = max(0, 100 - (weighted_violations / max_weighted_score * 100))
        
        return round(compliance, 2)
    
    def _determine_overall_risk(self, severity_breakdown: Dict[str, int], compliance_score: float) -> str:
        """
        Determine overall risk level based on violations and compliance score.
        
        Args:
            severity_breakdown: Breakdown by severity
            compliance_score: Compliance percentage
            
        Returns:
            Risk level string: "critical", "high", "moderate", or "low"
        """
        high_count = severity_breakdown.get("high", 0)
        medium_count = severity_breakdown.get("medium", 0)
        
        # Critical risk: multiple high severity violations or very low compliance
        if high_count >= Config.HIGH_SEVERITY_THRESHOLD or compliance_score < 50:
            return "critical"
        
        # High risk: any high severity violations or low compliance
        if high_count > 0 or compliance_score < 70:
            return "high"
        
        # Moderate risk: multiple medium violations or moderate compliance
        if medium_count > 3 or compliance_score < 85:
            return "moderate"
        
        # Low risk: few issues and good compliance
        return "low"
    
    def _determine_audit_result(self, risk_score: RiskScore) -> bool:
        """
        Determine if the audit passed based on configured thresholds.
        
        Args:
            risk_score: Calculated risk score
            
        Returns:
            True if audit passed, False otherwise
        """
        # Fail if compliance below threshold
        if risk_score["compliance_percentage"] < Config.COMPLIANCE_PASS_THRESHOLD:
            return False
        
        # Fail if too many high severity issues
        if risk_score["high_count"] >= Config.HIGH_SEVERITY_THRESHOLD:
            return False
        
        # Fail if overall risk is critical
        if risk_score["overall_risk"] == "critical":
            return False
        
        return True
    
    def _classify_individual_violation(self, violation: Violation) -> Dict[str, any]:
        """
        Provide additional classification details for a violation.
        
        Args:
            violation: Violation to classify
            
        Returns:
            Classification metadata
        """
        classification = {
            "severity": violation["severity"].value,
            "confidence": violation["confidence"],
            "requires_immediate_action": violation["severity"] == SeverityLevel.HIGH,
            "impact_category": self._determine_impact_category(violation)
        }
        
        return classification
    
    def _determine_impact_category(self, violation: Violation) -> str:
        """
        Determine the impact category of a violation.
        
        Args:
            violation: Violation to categorize
            
        Returns:
            Impact category string
        """
        rule_id = violation["rule_id"]
        
        if rule_id.startswith("SEC"):
            return "security"
        elif rule_id.startswith("DOC"):
            return "documentation"
        elif rule_id.startswith("PRIV"):
            return "privacy"
        else:
            return "general"


def risk_classification_node(state: ComplianceState) -> ComplianceState:
    """
    LangGraph node function for risk classification.
    
    Args:
        state: Current compliance state
        
    Returns:
        Updated state with risk scores
    """
    node = RiskClassificationNode()
    return node.execute(state)