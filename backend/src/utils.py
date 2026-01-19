"""
Utility functions for the Compliance Audit Agent.
Helper functions for common operations.
"""

import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path


def ensure_directory_exists(path: str) -> None:
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        path: Directory path
    """
    os.makedirs(path, exist_ok=True)


def load_json_file(file_path: str) -> Optional[Dict]:
    """
    Load and parse a JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {str(e)}")
        return None


def save_json_file(data: Dict, file_path: str) -> bool:
    """
    Save data as JSON file.
    
    Args:
        data: Data to save
        file_path: Output file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        ensure_directory_exists(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON file {file_path}: {str(e)}")
        return False


def read_text_file(file_path: str) -> Optional[str]:
    """
    Read text file content.
    
    Args:
        file_path: Path to text file
        
    Returns:
        File content or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return None


def write_text_file(content: str, file_path: str) -> bool:
    """
    Write content to text file.
    
    Args:
        content: Content to write
        file_path: Output file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        ensure_directory_exists(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file {file_path}: {str(e)}")
        return False


def list_files_in_directory(directory: str, extensions: List[str] = None) -> List[str]:
    """
    List all files in a directory with optional extension filter.
    
    Args:
        directory: Directory to scan
        extensions: Optional list of extensions to filter (e.g., ['.txt', '.py'])
        
    Returns:
        List of file paths
    """
    if not os.path.exists(directory):
        return []
    
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if extensions:
                if Path(file_path).suffix in extensions:
                    files.append(file_path)
            else:
                files.append(file_path)
    
    return files


def format_timestamp(timestamp_str: str, format_style: str = "readable") -> str:
    """
    Format timestamp string in different styles.
    
    Args:
        timestamp_str: ISO format timestamp
        format_style: "readable", "short", or "iso"
        
    Returns:
        Formatted timestamp
    """
    from datetime import datetime
    
    try:
        dt = datetime.fromisoformat(timestamp_str)
        
        if format_style == "readable":
            return dt.strftime("%B %d, %Y at %I:%M %p")
        elif format_style == "short":
            return dt.strftime("%Y-%m-%d %H:%M")
        else:  # iso
            return timestamp_str
    except Exception:
        return timestamp_str


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def calculate_file_size_mb(file_path: str) -> float:
    """
    Calculate file size in megabytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        Size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return round(size_bytes / (1024 * 1024), 2)
    except Exception:
        return 0.0


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    return sanitized


def create_summary_dict(state: Dict) -> Dict[str, Any]:
    """
    Create a summary dictionary from state for logging.
    
    Args:
        state: Compliance state
        
    Returns:
        Summary dictionary
    """
    summary = {
        "documents_count": len(state.get("documents", [])),
        "rules_count": len(state.get("rules", [])),
        "violations_count": len(state.get("violations", [])),
        "processing_stage": state.get("processing_stage", "unknown"),
        "errors_count": len(state.get("errors", [])),
        "warnings_count": len(state.get("warnings", []))
    }
    
    risk_scores = state.get("risk_scores")
    if risk_scores:
        summary["compliance_score"] = risk_scores.get("compliance_percentage", 0)
        summary["overall_risk"] = risk_scores.get("overall_risk", "unknown")
    
    return summary


def validate_environment() -> bool:
    """
    Validate that the environment is properly configured.
    
    Returns:
        True if valid, False otherwise
    """
    from config import Config
    
    issues = []
    
    # Check API key
    if not Config.GROK_API_KEY:
        issues.append("GROK_API_KEY not set in environment")
    
    # Check required directories
    required_dirs = [
        Config.MOCK_DOCS_PATH,
        Config.MOCK_RULES_PATH,
        Config.MOCK_REPO_PATH
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            issues.append(f"Required directory not found: {dir_path}")
    
    if issues:
        print("Environment validation failed:")
        for issue in issues:
            print(f"  ⚠️  {issue}")
        return False
    
    return True


def setup_mock_environment() -> bool:
    """
    Set up mock directories and files for testing.
    
    Returns:
        True if successful
    """
    from config import Config
    
    try:
        # Create directories
        ensure_directory_exists(Config.MOCK_DOCS_PATH)
        ensure_directory_exists(Config.MOCK_RULES_PATH)
        ensure_directory_exists(Config.MOCK_REPO_PATH)
        ensure_directory_exists(Config.OUTPUT_PATH)
        
        print("✓ Mock environment directories created")
        return True
        
    except Exception as e:
        print(f"✗ Failed to set up mock environment: {str(e)}")
        return False


def print_state_summary(state: Dict) -> None:
    """
    Print a formatted summary of the current state.
    
    Args:
        state: Compliance state
    """
    summary = create_summary_dict(state)
    
    print("\n" + "="*60)
    print("STATE SUMMARY")
    print("="*60)
    print(f"Processing Stage: {summary['processing_stage']}")
    print(f"Documents: {summary['documents_count']}")
    print(f"Rules: {summary['rules_count']}")
    print(f"Violations: {summary['violations_count']}")
    
    if "compliance_score" in summary:
        print(f"Compliance: {summary['compliance_score']:.1f}%")
        print(f"Risk Level: {summary['overall_risk']}")
    
    if summary['errors_count'] > 0:
        print(f"Errors: {summary['errors_count']}")
    if summary['warnings_count'] > 0:
        print(f"Warnings: {summary['warnings_count']}")
    
    print("="*60 + "\n")