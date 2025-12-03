from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import subprocess
import tempfile
import shutil
from jinja2 import Environment, FileSystemLoader
from pdf2docx import Converter

app = FastAPI(title="CV Standardization API", version="1.0.0")

# -------------------------------------------------------
# MODELS
# -------------------------------------------------------
class PersonalInfo(BaseModel):
    full_name: str
    role: str
    department: str
    seniority: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class KeySkill(BaseModel):
    category: str
    items: List[str]

class Certification(BaseModel):
    name: str
    code: str
    year: str

class Language(BaseModel):
    language: str
    level: str

class Experience(BaseModel):
    role: str
    company: str
    start_date: str
    end_date: str
    description_list: List[str]

class CVData(BaseModel):
    id: str
    personal_info: PersonalInfo
    summary: str
    key_achievements: List[str]
    key_skills: List[KeySkill]
    certifications: List[Certification]
    languages: List[Language]
    experience: List[Experience]

# -------------------------------------------------------
# LATEX ESCAPE FILTER
# -------------------------------------------------------
def latex_escape(text):
    """Escapa caratteri speciali LaTeX"""
    if text is None:
        return ""
    
    text = str(text)
    
    replacements = [
        ('\\', r'\textbackslash '),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde '),
        ('^', r'\^{}'),
    ]
    
    for old, new in replacements:
        text = text.replace(old, new)
    
    return text

# -------------------------------------------------------
# CV GENERATION FUNCTION
# -------------------------------------------------------
def generate_cv(cv_data: dict, output_dir: str):
    """Generate CV in PDF and DOCX format"""
    
    # Setup Jinja2 environment
    env = Environment(
        loader=FileSystemLoader("template"),
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<#",
        comment_end_string="#>"
    )
    env.filters['tex'] = latex_escape
    
    # Add logo path
    cv_data["logo_path"] = os.path.abspath("assets/cluster_reply_logo.jpg")
    
    # Render LaTeX template
    template = env.get_template("cv_template.tex")
    latex_output = template.render(**cv_data)
    
    # Write .tex file
    tex_path = os.path.join(output_dir, "cv_output.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_output)
    
    # Compile LaTeX to PDF
    for i in range(2):  # Run twice for references
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
            capture_output=True,
            text=True,
            check=False
        )
    
    pdf_path = os.path.join(output_dir, "cv_output.pdf")
    
    if not os.path.exists(pdf_path):
        raise Exception("PDF generation failed")
    
    # Convert PDF to DOCX
    docx_path = os.path.join(output_dir, "cv_output.docx")
    cv_converter = Converter(pdf_path)
    cv_converter.convert(docx_path)
    cv_converter.close()
    
    # Cleanup auxiliary files
    for ext in ['.aux', '.log', '.out', '.tex']:
        aux_file = os.path.join(output_dir, f"cv_output{ext}")
        if os.path.exists(aux_file):
            os.remove(aux_file)
    
    return pdf_path, docx_path

# -------------------------------------------------------
# API ENDPOINTS
# -------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "CV Standardization API",
        "version": "1.0.0",
        "endpoints": {
            "POST /generate-cv": "Generate CV in PDF and DOCX format",
            "GET /health": "Health check"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/generate-cv")
def generate_cv_endpoint(cv_data: CVData):
    """
    Generate CV from JSON data
    Returns: URLs to download PDF and DOCX
    """
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Convert Pydantic model to dict
        cv_dict = cv_data.model_dump()
        
        # Generate CV
        pdf_path, docx_path = generate_cv(cv_dict, temp_dir)
        
        # In production, you'd upload these to cloud storage and return URLs
        # For now, return success message with file paths
        return {
            "status": "success",
            "message": "CV generated successfully",
            "pdf_path": pdf_path,
            "docx_path": docx_path,
            "note": "Files are in temporary directory. In production, implement file download endpoints."
        }
        
    except Exception as e:
        # Cleanup temp directory on error
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

# Note: For production, add these endpoints:
# @app.get("/download-pdf/{file_id}")
# @app.get("/download-docx/{file_id}")