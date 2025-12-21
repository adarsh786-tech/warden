"""
Report Generation Node - Creates structured audit report.
Consolidates findings into a comprehensive, actionable summary.
"""

from datetime import datetime
from typing import List, Dict
from src.state import ComplianceState, AuditReport, Violation, SeverityLevel
from src.config import Config


class ReportGenerationNode:
    """
    Generates a structured, human-readable audit report.
    Consolidates all findings, scores, and recommendations.
    """
    
    def execute(self, state: ComplianceState) -> ComplianceState:
        """
        Main execution function for report generation.
        
        Args:
            state: Current compliance state
            
        Returns:
            Updated state with final audit report
        """
        try:
            state["processing_stage"] = "report_generation"
            
            # Generate the audit report
            report = self._generate_audit_report(state)
            state["final_report"] = report
            
            if Config.VERBOSE:
                print("✓ Audit report generated")
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Report generation error: {str(e)}")
            print(f"✗ Report generation failed: {str(e)}")
            return state
    
    def _generate_audit_report(self, state: ComplianceState) -> AuditReport:
        """
        Generate the complete audit report.
        
        Args:
            state: Current compliance state
            
        Returns:
            Structured audit report
        """
        risk_scores = state.get("risk_scores")
        violations = state.get("violations", [])
        
        # Generate recommendations
        recommendations = self._generate_recommendations(violations, risk_scores)
        
        # Identify missing artifacts
        missing_artifacts = self._identify_missing_artifacts(state)
        
        # Generate summary text
        summary = self._generate_summary(state, risk_scores, violations)
        
        # Create traceable evidence
        traceable_evidence = self._create_traceable_evidence(state)
        
        report: AuditReport = {
            "timestamp": datetime.now().isoformat(),
            "compliance_score": risk_scores["compliance_percentage"] if risk_scores else 0.0,
            "risk_assessment": risk_scores if risk_scores else self._empty_risk_score(),
            "violations": violations,
            "missing_artifacts": missing_artifacts,
            "recommendations": recommendations,
            "summary": summary,
            "traceable_evidence": traceable_evidence
        }
        
        return report
    
    def _generate_recommendations(
        self, 
        violations: List[Violation], 
        risk_scores: Dict
    ) -> List[str]:
        """
        Generate actionable recommendations based on violations.
        
        Args:
            violations: List of violations
            risk_scores: Risk assessment scores
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Group violations by rule
        violations_by_rule = {}
        for v in violations:
            rule_id = v["rule_id"]
            if rule_id not in violations_by_rule:
                violations_by_rule[rule_id] = []
            violations_by_rule[rule_id].append(v)
        
        # Generate recommendations for high severity violations first
        high_severity = [v for v in violations if v["severity"] == SeverityLevel.HIGH]
        for violation in high_severity:
            rec = self._create_recommendation_for_violation(violation)
            if rec and rec not in recommendations:
                recommendations.append(rec)
        
        # Add general recommendations based on patterns
        if any("password" in v["evidence"].lower() for v in violations):
            recommendations.append("Implement secure password hashing using bcrypt or argon2")
        
        if any("api" in v["evidence"].lower() or "key" in v["evidence"].lower() for v in violations):
            recommendations.append("Move all API keys and secrets to environment variables or secure vault")
        
        if any("logging" in v["rule_name"].lower() for v in violations):
            recommendations.append("Enable comprehensive logging for security-relevant events")
        
        if any("readme" in v["rule_name"].lower() for v in violations):
            recommendations.append("Create comprehensive README.md with setup and usage instructions")
        
        # If many violations, recommend systematic review
        if len(violations) > 10:
            recommendations.append("Conduct systematic security review and implement compliance framework")
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def _create_recommendation_for_violation(self, violation: Violation) -> str:
        """
        Create a specific recommendation for a violation.
        
        Args:
            violation: Violation to create recommendation for
            
        Returns:
            Recommendation string
        """
        rule_id = violation["rule_id"]
        
        # Map rule IDs to recommendations
        recommendation_map = {
            "SEC-001": "Encrypt all passwords using approved algorithms (bcrypt, argon2, PBKDF2)",
            "SEC-002": "Remove hardcoded API keys and use environment variables",
            "SEC-003": "Implement input validation and sanitization for all user inputs",
            "SEC-004": "Enable logging for authentication, authorization, and critical operations",
            "SEC-005": "Use HTTPS/TLS for all network communications",
            "DOC-001": "Create a README.md file with project overview and setup instructions",
            "DOC-002": "Document security policies and incident response procedures",
            "DOC-003": "Create dependency manifest (requirements.txt, package.json, etc.)",
            "PRIV-001": "Document PII handling, collection, and storage policies",
            "PRIV-002": "Define and document data retention and deletion policies"
        }
        
        return recommendation_map.get(rule_id, f"Address violation: {violation['rule_name']}")
    
    def _identify_missing_artifacts(self, state: ComplianceState) -> List[str]:
        """
        Identify missing documentation or artifacts.
        
        Args:
            state: Current compliance state
            
        Returns:
            List of missing artifact descriptions
        """
        missing = []
        
        # Check for common missing files
        doc_files = [doc["metadata"]["file_name"].lower() for doc in state["documents"]]
        
        if not any("readme" in f for f in doc_files):
            missing.append("README.md - Project documentation")
        
        if not any("security" in f for f in doc_files):
            missing.append("SECURITY.md - Security policy documentation")
        
        if not any("requirements" in f or "package" in f for f in doc_files):
            missing.append("Dependency manifest (requirements.txt, package.json)")
        
        if not any("license" in f for f in doc_files):
            missing.append("LICENSE - License information")
        
        # Check for violations indicating missing artifacts
        for violation in state["violations"]:
            if "must exist" in violation["explanation"].lower():
                artifact = violation["rule_name"].replace(" Required", "").replace(" Must Exist", "")
                if artifact not in missing:
                    missing.append(artifact)
        
        return missing
    
    def _generate_summary(
        self, 
        state: ComplianceState, 
        risk_scores: Dict, 
        violations: List[Violation]
    ) -> str:
        """
        Generate executive summary text.
        
        Args:
            state: Current compliance state
            risk_scores: Risk assessment
            violations: List of violations
            
        Returns:
            Summary text
        """
        if not risk_scores:
            return "Audit incomplete - no risk assessment available"
        
        compliance_pct = risk_scores["compliance_percentage"]
        total_issues = risk_scores["total_issues"]
        high_count = risk_scores["high_count"]
        medium_count = risk_scores["medium_count"]
        low_count = risk_scores["low_count"]
        overall_risk = risk_scores["overall_risk"]
        
        audit_result = "PASSED" if state["audit_passed"] else "FAILED"
        
        summary = f"""Compliance Audit Summary
========================

Audit Result: {audit_result}
Compliance Score: {compliance_pct:.1f}%
Overall Risk Level: {overall_risk.upper()}

Issue Breakdown:
- Critical Issues: {high_count}
- Moderate Issues: {medium_count}
- Low Priority Issues: {low_count}
- Total Issues: {total_issues}

Documents Analyzed: {len(state['documents'])}
Rules Evaluated: {len(state['rules'])}
"""
        
        if state["reflection_notes"]:
            summary += f"Reflection Iterations: {len(state['reflection_notes'])}\n"
        
        if high_count > 0:
            summary += f"\n⚠️  {high_count} CRITICAL issue(s) require immediate attention.\n"
        
        if not state["audit_passed"]:
            summary += "\nThe project does not meet minimum compliance requirements.\n"
            summary += "Review the recommendations section for required remediation steps.\n"
        else:
            summary += "\nThe project meets minimum compliance requirements.\n"
            summary += "Address remaining issues to improve security posture.\n"
        
        return summary
    
    def _create_traceable_evidence(self, state: ComplianceState) -> Dict:
        """
        Create traceable evidence linking violations to sources.
        
        Args:
            state: Current compliance state
            
        Returns:
            Evidence traceability dictionary
        """
        evidence = {
            "audit_timestamp": datetime.now().isoformat(),
            "documents_analyzed": [
                {
                    "source": doc["source"],
                    "type": doc["doc_type"],
                    "size": doc["metadata"]["size_bytes"]
                }
                for doc in state["documents"]
            ],
            "rules_applied": [
                {
                    "rule_id": rule["rule_id"],
                    "name": rule["name"],
                    "category": rule["category"]
                }
                for rule in state["rules"]
            ],
            "violation_evidence": [
                {
                    "rule_id": v["rule_id"],
                    "location": v.get("location"),
                    "evidence_snippet": v["evidence"][:200]  # First 200 chars
                }
                for v in state["violations"]
            ],
            "reflection_performed": len(state["reflection_notes"]) > 0,
            "execution_metadata": state.get("execution_metadata", {})
        }
        
        return evidence
    
    def _empty_risk_score(self) -> Dict:
        """Return empty risk score structure."""
        return {
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0,
            "total_issues": 0,
            "compliance_percentage": 0.0,
            "overall_risk": "unknown"
        }


def report_generation_node(state: ComplianceState) -> ComplianceState:
    """
    LangGraph node function for report generation.
    
    Args:
        state: Current compliance state
        
    Returns:
        Updated state with final report
    """
    node = ReportGenerationNode()
    return node.execute(state)