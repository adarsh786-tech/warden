"""
Output Dispatcher Node - Formats and delivers final audit results.
Prepares output for CLI display, file export, or API response.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any
from src.state import ComplianceState, AuditReport
from src.config import Config


class OutputDispatcherNode:
    """
    Handles final output formatting and delivery.
    Supports multiple output formats: console, JSON, HTML.
    """
    
    def __init__(self):
        self.output_formats = ["console", "json", "summary"]
    
    def execute(self, state: ComplianceState) -> ComplianceState:
        """
        Main execution function for output dispatch.
        
        Args:
            state: Current compliance state
            
        Returns:
            Final state (unchanged, output is side effect)
        """
        try:
            state["processing_stage"] = "output_dispatch"
            
            report = state.get("final_report")
            
            if not report:
                print("✗ No report available to output")
                return state
            
            # Display console output
            self._display_console_output(state, report)
            
            # Save JSON report
            self._save_json_report(report)
            
            # Save summary report
            self._save_summary_report(report, state)
            
            if Config.VERBOSE:
                print("\n✓ Output dispatch complete")
                print(f"  Reports saved to: {Config.OUTPUT_PATH}")
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Output dispatch error: {str(e)}")
            print(f"✗ Output dispatch failed: {str(e)}")
            return state
    
    def _display_console_output(self, state: ComplianceState, report: AuditReport):
        """
        Display formatted output to console.
        
        Args:
            state: Current compliance state
            report: Audit report
        """
        print("\n" + "="*80)
        print("COMPLIANCE AUDIT REPORT")
        print("="*80)
        print(report["summary"])
        
        # Display violations by severity
        if report["violations"]:
            print("\n" + "-"*80)
            print("VIOLATIONS FOUND")
            print("-"*80)
            
            high_violations = [v for v in report["violations"] if v["severity"].value == "high"]
            medium_violations = [v for v in report["violations"] if v["severity"].value == "medium"]
            low_violations = [v for v in report["violations"] if v["severity"].value == "low"]
            
            if high_violations:
                print("\n🔴 CRITICAL SEVERITY:")
                for v in high_violations:
                    self._print_violation(v)
            
            if medium_violations:
                print("\n🟡 MODERATE SEVERITY:")
                for v in medium_violations:
                    self._print_violation(v)
            
            if low_violations:
                print("\n🟢 LOW SEVERITY:")
                for v in low_violations:
                    self._print_violation(v)
        
        # Display missing artifacts
        if report["missing_artifacts"]:
            print("\n" + "-"*80)
            print("MISSING ARTIFACTS")
            print("-"*80)
            for artifact in report["missing_artifacts"]:
                print(f"  • {artifact}")
        
        # Display recommendations
        if report["recommendations"]:
            print("\n" + "-"*80)
            print("RECOMMENDATIONS")
            print("-"*80)
            for i, rec in enumerate(report["recommendations"], 1):
                print(f"  {i}. {rec}")
        
        # Display errors if any
        if state.get("errors"):
            print("\n" + "-"*80)
            print("ERRORS ENCOUNTERED")
            print("-"*80)
            for error in state["errors"]:
                print(f"  ⚠️  {error}")
        
        print("\n" + "="*80)
    
    def _print_violation(self, violation: Dict):
        """
        Print a single violation in formatted style.
        
        Args:
            violation: Violation dictionary
        """
        print(f"\n  [{violation['rule_id']}] {violation['rule_name']}")
        print(f"  Location: {violation.get('location', 'Not specified')}")
        print(f"  Confidence: {violation['confidence']*100:.0f}%")
        print(f"  Evidence: {violation['evidence'][:150]}...")
        print(f"  Explanation: {violation['explanation']}")
    
    def _save_json_report(self, report: AuditReport):
        """
        Save the audit report as JSON file.
        
        Args:
            report: Audit report
        """
        # Create output directory if it doesn't exist
        os.makedirs(Config.OUTPUT_PATH, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audit_report_{timestamp}.json"
        filepath = os.path.join(Config.OUTPUT_PATH, filename)
        
        # Convert report to JSON-serializable format
        json_report = self._prepare_json_serializable(report)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 JSON report saved: {filepath}")
    
    def _save_summary_report(self, report: AuditReport, state: ComplianceState):
        """
        Save a human-readable summary report.
        
        Args:
            report: Audit report
            state: Current compliance state
        """
        os.makedirs(Config.OUTPUT_PATH, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audit_summary_{timestamp}.txt"
        filepath = os.path.join(Config.OUTPUT_PATH, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("COMPLIANCE AUDIT SUMMARY REPORT\n")
            f.write("="*80 + "\n\n")
            f.write(report["summary"])
            f.write("\n\n")
            
            # Write violations
            if report["violations"]:
                f.write("-"*80 + "\n")
                f.write("DETAILED VIOLATIONS\n")
                f.write("-"*80 + "\n\n")
                
                for v in report["violations"]:
                    f.write(f"[{v['rule_id']}] {v['rule_name']}\n")
                    f.write(f"Severity: {v['severity'].value.upper()}\n")
                    f.write(f"Location: {v.get('location', 'Not specified')}\n")
                    f.write(f"Confidence: {v['confidence']*100:.0f}%\n")
                    f.write(f"Evidence: {v['evidence']}\n")
                    f.write(f"Explanation: {v['explanation']}\n")
                    f.write("\n")
            
            # Write recommendations
            if report["recommendations"]:
                f.write("-"*80 + "\n")
                f.write("RECOMMENDATIONS\n")
                f.write("-"*80 + "\n\n")
                for i, rec in enumerate(report["recommendations"], 1):
                    f.write(f"{i}. {rec}\n")
                f.write("\n")
            
            # Write missing artifacts
            if report["missing_artifacts"]:
                f.write("-"*80 + "\n")
                f.write("MISSING ARTIFACTS\n")
                f.write("-"*80 + "\n\n")
                for artifact in report["missing_artifacts"]:
                    f.write(f"• {artifact}\n")
                f.write("\n")
            
            f.write("="*80 + "\n")
            f.write(f"Report generated: {report['timestamp']}\n")
            f.write("="*80 + "\n")
        
        print(f"📄 Summary report saved: {filepath}")
    
    def _prepare_json_serializable(self, obj: Any) -> Any:
        """
        Convert objects to JSON-serializable format.
        
        Args:
            obj: Object to convert
            
        Returns:
            JSON-serializable version
        """
        if isinstance(obj, dict):
            return {k: self._prepare_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._prepare_json_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return self._prepare_json_serializable(obj.__dict__)
        elif hasattr(obj, 'value'):  # For Enums
            return obj.value
        else:
            return obj


def output_dispatcher_node(state: ComplianceState) -> ComplianceState:
    """
    LangGraph node function for output dispatch.
    
    Args:
        state: Current compliance state
        
    Returns:
        Final state (unchanged)
    """
    node = OutputDispatcherNode()
    return node.execute(state)