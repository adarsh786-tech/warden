"""
Ingestion Node - Handles document and repository file ingestion.
Normalizes, segments, and prepares content for compliance evaluation.
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from src.state import ComplianceState, DocumentBlock
from src.config import Config
import PyPDF2


class IngestionNode:
    """
    Responsible for ingesting and preprocessing all input documents.
    Accepts mock documentation and repository files, then normalizes them.
    """
    
    def __init__(self):
        self.supported_extensions = {'.txt', '.md', '.py', '.json', '.yaml', '.yml', '.xml', '.pdf'}
    
    def execute(self, state: ComplianceState) -> ComplianceState:
        """
        Main execution function for the ingestion node.
        
        Args:
            state: Current compliance state
            
        Returns:
            Updated state with processed documents
        """
        try:
            state["processing_stage"] = "ingestion"
            
            # Collect all input paths
            # If paths are already in state (from API upload), use those
            # Otherwise, gather from configured directories
            if state.get("raw_input_paths"):
                input_paths = state["raw_input_paths"]
                if Config.VERBOSE:
                    print(f"Using {len(input_paths)} uploaded file(s)")
            else:
                input_paths = self._gather_input_paths()
                state["raw_input_paths"] = input_paths
                if Config.VERBOSE:
                    print(f"Gathered {len(input_paths)} file(s) from configured directories")
            
            # Process each file
            documents = []
            for path in input_paths:
                doc_blocks = self._process_file(path)
                documents.extend(doc_blocks)
            
            state["documents"] = documents
            
            if Config.VERBOSE:
                print(f"✓ Ingestion complete: {len(documents)} document blocks processed")
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Ingestion error: {str(e)}")
            print(f"✗ Ingestion failed: {str(e)}")
            return state
    
    def _gather_input_paths(self) -> List[str]:
        """Gather all file paths from configured directories."""
        paths = []
        
        # Collect from mock docs
        if os.path.exists(Config.MOCK_DOCS_PATH):
            paths.extend(self._scan_directory(Config.MOCK_DOCS_PATH))
        
        # Collect from mock repository
        if os.path.exists(Config.MOCK_REPO_PATH):
            paths.extend(self._scan_directory(Config.MOCK_REPO_PATH))
        
        return paths
    
    def _scan_directory(self, directory: str) -> List[str]:
        """Recursively scan directory for supported files."""
        file_paths = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if Path(file_path).suffix in self.supported_extensions:
                    file_paths.append(file_path)
        
        return file_paths
    
    def _process_file(self, file_path: str) -> List[DocumentBlock]:
        """
        Process a single file and convert it to document blocks.
        
        Args:
            file_path: Path to the file
            
        Returns:
            List of document blocks (may split large files)
        """
        try:
            # Handle PDF files differently
            if file_path.endswith('.pdf'):
                content = self._extract_pdf_text(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # Determine document type
            doc_type = self._classify_document_type(file_path, content)
            
            # Clean and normalize content
            normalized_content = self._normalize_content(content)
            
            # Create document block
            doc_block: DocumentBlock = {
                "source": file_path,
                "content": normalized_content,
                "doc_type": doc_type,
                "metadata": {
                    "file_name": os.path.basename(file_path),
                    "file_extension": Path(file_path).suffix,
                    "size_bytes": len(content),
                    "line_count": content.count('\n') + 1
                }
            }
            
            # For very large files, could split into chunks here
            # For now, return as single block
            return [doc_block]
            
        except Exception as e:
            print(f"Warning: Could not process {file_path}: {str(e)}")
            return []
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """
        Extract text from PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            
            
            text = []
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if Config.VERBOSE:
                    print(f"  Extracting text from PDF: {os.path.basename(file_path)} ({len(pdf_reader.pages)} pages)")
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            
            extracted_text = '\n'.join(text)
            
            if not extracted_text.strip():
                raise Exception("No text could be extracted from PDF")
            
            return extracted_text
            
        except ImportError:
            raise Exception("PyPDF2 is required to process PDF files. Install it with: pip install PyPDF2")
        except Exception as e:
            raise Exception(f"Failed to extract PDF text: {str(e)}")
    
    def _classify_document_type(self, file_path: str, content: str) -> str:
        """
        Classify the document type based on path and content.
        
        Returns:
            Document type string
        """
        file_path_lower = file_path.lower()
        
        # Check by filename patterns
        if 'readme' in file_path_lower:
            return 'readme'
        elif 'policy' in file_path_lower or 'compliance' in file_path_lower:
            return 'policy'
        elif 'config' in file_path_lower or file_path.endswith(('.json', '.yaml', '.yml', '.xml')):
            return 'config'
        elif file_path.endswith('.py'):
            return 'code'
        elif 'requirement' in file_path_lower or 'spec' in file_path_lower:
            return 'requirements'
        elif 'log' in file_path_lower:
            return 'logs'
        elif file_path.endswith('.pdf'):
            # Try to infer PDF type from content
            content_lower = content.lower()
            if 'resume' in content_lower or 'curriculum vitae' in content_lower or 'cv' in file_path_lower:
                return 'resume'
            elif 'policy' in content_lower or 'compliance' in content_lower:
                return 'policy'
            elif 'requirement' in content_lower or 'specification' in content_lower:
                return 'requirements'
            else:
                return 'documentation'
        else:
            return 'documentation'
    
    def _normalize_content(self, content: str) -> str:
        """
        Normalize and clean document content.
        
        Args:
            content: Raw file content
            
        Returns:
            Normalized content
        """
        # Remove excessive whitespace
        lines = content.split('\n')
        cleaned_lines = [line.rstrip() for line in lines]
        
        # Remove multiple consecutive empty lines
        normalized_lines = []
        prev_empty = False
        
        for line in cleaned_lines:
            if line.strip() == '':
                if not prev_empty:
                    normalized_lines.append(line)
                prev_empty = True
            else:
                normalized_lines.append(line)
                prev_empty = False
        
        return '\n'.join(normalized_lines)


def ingestion_node(state: ComplianceState) -> ComplianceState:
    """
    LangGraph node function for ingestion.
    
    Args:
        state: Current compliance state
        
    Returns:
        Updated state with ingested documents
    """
    node = IngestionNode()
    return node.execute(state)