"""
FastAPI application for Compliance Audit Agent.
Simple API wrapper around the existing LangGraph workflow.
"""

import os
import shutil
import uuid
from pathlib import Path
from typing import List
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import existing components
from src.config import Config
from src.graph import create_compliance_audit_graph

# Initialize FastAPI app
app = FastAPI(
    title="Compliance Audit API",
    description="AI-powered compliance checker for code and documentation",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload directory exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Compliance Audit API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "GET /health",
            "audit": "POST /audit"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "grok_api_configured": bool(Config.GROQ_API_KEY)
    }


@app.post("/audit")
async def run_audit(files: List[UploadFile] = File(...)):
    """
    Run compliance audit on uploaded files.
    
    Args:
        files: List of files to audit (code, documentation, configs)
        
    Returns:
        Audit results with compliance score, violations, and recommendations
    """
    
    # Validate files
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # Create unique session ID for this audit
    session_id = str(uuid.uuid4())
    session_folder = os.path.join(Config.UPLOAD_FOLDER, session_id)
    os.makedirs(session_folder, exist_ok=True)
    
    uploaded_file_paths = []
    
    try:
        # Save uploaded files
        for file in files:
            # Validate file extension
            file_ext = Path(file.filename).suffix
            if file_ext not in Config.ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type {file_ext} not allowed. Allowed: {Config.ALLOWED_EXTENSIONS}"
                )
            
            # Check file size
            file.file.seek(0, 2)  # Seek to end
            file_size = file.file.tell()
            file.file.seek(0)  # Reset to beginning
            
            if file_size > Config.MAX_UPLOAD_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} exceeds maximum size of {Config.MAX_UPLOAD_SIZE} bytes"
                )
            
            # Save file
            file_path = os.path.join(session_folder, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded_file_paths.append(file_path)
        graph = create_compliance_audit_graph()
        result = graph.run_api(uploaded_file_paths)
        result["metadata"]["sessionId"] = session_id
        
        return JSONResponse(content=result)
    
    except Exception as e:
        if os.path.exists(session_folder):
            shutil.rmtree(session_folder)
        
        raise HTTPException(
            status_code=500,
            detail=f"Audit failed: {str(e)}"
        )
    
    finally:
        try:
            if os.path.exists(session_folder):
                shutil.rmtree(session_folder)
        except Exception as e:
            print(f"Warning: Failed to clean up session folder: {str(e)}")

@app.get("/config")
def get_config():
    """
    Get current configuration (non-sensitive info only).
    """
    return {
        "model": Config.GROK_MODEL,
        "temperature": Config.TEMPERATURE,
        "compliance_threshold": Config.COMPLIANCE_PASS_THRESHOLD,
        "reflection_enabled": Config.ENABLE_REFLECTION,
        "max_reflection_iterations": Config.MAX_REFLECTION_ITERATIONS,
        "allowed_file_extensions": list(Config.ALLOWED_EXTENSIONS),
        "max_upload_size_mb": Config.MAX_UPLOAD_SIZE / (1024 * 1024)
    }


@app.get("/rules")
def list_available_rules():
    """
    List all available compliance rules.
    """
    from src.nodes.rule_retrieval import RuleRetrievalNode
    
    node = RuleRetrievalNode()
    default_rules = node.default_rules
    
    rules_info = []
    for rule in default_rules:
        rules_info.append({
            "rule_id": rule["rule_id"],
            "name": rule["name"],
            "category": rule["category"],
            "severity": rule["severity"].value,
            "description": rule["description"]
        })
    
    return {
        "total_rules": len(rules_info),
        "rules": rules_info
    }

