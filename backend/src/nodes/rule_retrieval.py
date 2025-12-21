"""
Rule Retrieval Node - Loads and prepares compliance rules.
Fetches relevant rules from the rule base and structures them for evaluation.
"""

import os
import json
from typing import List, Dict, Any
from src.state import ComplianceState, ComplianceRule, SeverityLevel
from src.config import Config


class RuleRetrievalNode:
    """
    Responsible for loading compliance rules from the rule base.
    Filters and prepares rules based on document types and categories.
    """
    
    def __init__(self):
        self.rules_cache: List[ComplianceRule] = []
        self.default_rules = self._get_default_rules()
    
    def execute(self, state: ComplianceState) -> ComplianceState:
        """
        Main execution function for rule retrieval.
        
        Args:
            state: Current compliance state
            
        Returns:
            Updated state with loaded compliance rules
        """
        try:
            state["processing_stage"] = "rule_retrieval"
            
            # Load rules from files or use defaults
            rules = self._load_rules_from_files()
            
            # If no custom rules found, use default rule set
            if not rules:
                rules = self.default_rules
                if Config.VERBOSE:
                    print("Using default compliance rules")
            
            # Filter rules based on document types present
            doc_types = set(doc["doc_type"] for doc in state["documents"])
            filtered_rules = self._filter_relevant_rules(rules, doc_types)
            
            state["rules"] = filtered_rules
            state["active_rule_categories"] = list(set(rule["category"] for rule in filtered_rules))
            
            if Config.VERBOSE:
                print(f"✓ Rule retrieval complete: {len(filtered_rules)} rules loaded")
                print(f"  Categories: {', '.join(state['active_rule_categories'])}")
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Rule retrieval error: {str(e)}")
            print(f"✗ Rule retrieval failed: {str(e)}")
            return state
    
    def _load_rules_from_files(self) -> List[ComplianceRule]:
        """Load rules from JSON files in the rules directory."""
        rules = []
        
        if not os.path.exists(Config.MOCK_RULES_PATH):
            return rules
        
        for file_name in os.listdir(Config.MOCK_RULES_PATH):
            if file_name.endswith('.json'):
                file_path = os.path.join(Config.MOCK_RULES_PATH, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        rule_data = json.load(f)
                        
                    # Handle both single rule and array of rules
                    if isinstance(rule_data, list):
                        rules.extend(self._validate_rules(rule_data))
                    else:
                        rules.append(self._validate_rule(rule_data))
                        
                except Exception as e:
                    print(f"Warning: Could not load rules from {file_name}: {str(e)}")
        
        return rules
    
    def _validate_rules(self, rules_data: List[Dict]) -> List[ComplianceRule]:
        """Validate and convert a list of rule dictionaries."""
        return [self._validate_rule(rule) for rule in rules_data]
    
    def _validate_rule(self, rule_data: Dict) -> ComplianceRule:
        """Validate and convert a single rule dictionary to ComplianceRule."""
        return ComplianceRule(
            rule_id=rule_data.get("rule_id", "UNKNOWN"),
            name=rule_data.get("name", "Unnamed Rule"),
            description=rule_data.get("description", ""),
            category=rule_data.get("category", "general"),
            severity=SeverityLevel(rule_data.get("severity", "medium")),
            criteria=rule_data.get("criteria", ""),
            examples=rule_data.get("examples", [])
        )
    
    def _filter_relevant_rules(self, rules: List[ComplianceRule], doc_types: set) -> List[ComplianceRule]:
        """
        Filter rules based on document types present.
        For now, return all rules. Can be enhanced with smart filtering.
        """
        # Future enhancement: filter based on doc_types
        # For example, only apply code-related rules if code documents exist
        return rules
    
    def _get_default_rules(self) -> List[ComplianceRule]:
        """
        Provide a default set of compliance rules for demonstration.
        These cover common security and documentation requirements.
        """
        return [
            ComplianceRule(
                rule_id="SEC-001",
                name="Password Encryption Required",
                description="All passwords must be encrypted using approved algorithms (bcrypt, argon2, PBKDF2)",
                category="security",
                severity=SeverityLevel.HIGH,
                criteria="Check for password storage without encryption. Look for plaintext password variables, unencrypted database fields, or direct password storage.",
                examples=["password = 'plaintext123'", "db.store('password', user_input)"]
            ),
            ComplianceRule(
                rule_id="SEC-002",
                name="API Keys Must Not Be Hardcoded",
                description="API keys and secrets must be stored in environment variables or secure vaults",
                category="security",
                severity=SeverityLevel.HIGH,
                criteria="Identify hardcoded API keys, tokens, or credentials in source code",
                examples=["API_KEY = 'sk-12345abcde'", "token = '0123456789abcdef'"]
            ),
            ComplianceRule(
                rule_id="SEC-003",
                name="Input Validation Required",
                description="All user inputs must be validated and sanitized to prevent injection attacks",
                category="security",
                severity=SeverityLevel.HIGH,
                criteria="Check for user input handling without validation or sanitization",
                examples=["query = f'SELECT * FROM users WHERE id={user_id}'"]
            ),
            ComplianceRule(
                rule_id="SEC-004",
                name="Logging Must Be Enabled",
                description="Security-relevant events must be logged with appropriate detail",
                category="security",
                severity=SeverityLevel.MEDIUM,
                criteria="Verify presence of logging for authentication, authorization, and critical operations",
                examples=[]
            ),
            ComplianceRule(
                rule_id="SEC-005",
                name="HTTPS/TLS Required",
                description="All network communications must use HTTPS/TLS encryption",
                category="security",
                severity=SeverityLevel.HIGH,
                criteria="Check for HTTP URLs or unencrypted network connections",
                examples=["http://api.example.com", "socket without TLS"]
            ),
            ComplianceRule(
                rule_id="DOC-001",
                name="README Must Exist",
                description="Project must include a README with setup instructions and overview",
                category="documentation",
                severity=SeverityLevel.MEDIUM,
                criteria="Check for presence of README.md or README.txt",
                examples=[]
            ),
            ComplianceRule(
                rule_id="DOC-002",
                name="Security Policy Required",
                description="Project must document security policies and incident response procedures",
                category="documentation",
                severity=SeverityLevel.MEDIUM,
                criteria="Look for security policy documentation or SECURITY.md file",
                examples=[]
            ),
            ComplianceRule(
                rule_id="DOC-003",
                name="Dependencies Must Be Documented",
                description="All dependencies and their versions must be documented",
                category="documentation",
                severity=SeverityLevel.LOW,
                criteria="Check for requirements.txt, package.json, or similar dependency manifests",
                examples=[]
            ),
            ComplianceRule(
                rule_id="PRIV-001",
                name="PII Handling Documented",
                description="Handling of personally identifiable information must be documented",
                category="data-privacy",
                severity=SeverityLevel.HIGH,
                criteria="Verify documentation of data collection, storage, and retention policies",
                examples=[]
            ),
            ComplianceRule(
                rule_id="PRIV-002",
                name="Data Retention Policy",
                description="Clear data retention and deletion policies must be defined",
                category="data-privacy",
                severity=SeverityLevel.MEDIUM,
                criteria="Check for documented data lifecycle and retention schedules",
                examples=[]
            )
        ]


def rule_retrieval_node(state: ComplianceState) -> ComplianceState:
    """
    LangGraph node function for rule retrieval.
    
    Args:
        state: Current compliance state
        
    Returns:
        Updated state with compliance rules
    """
    node = RuleRetrievalNode()
    return node.execute(state)