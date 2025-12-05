# CV Standardization Backend

**Automated CV generation API for Cluster Reply**

Provide a CV and a staffing request, and generate client-ready CVs in PDF and DOCX format in under 5 minutes, directly from Microsoft 365 Copilot.

---

## 📋 Project Overview

This project provides a REST API backend that integrates with **Microsoft Copilot Studio** to automate the creation of standardized Cluster Reply CVs. 


### The Solution
An AI-powered workflow that:
1. **Extracts** information from candidate CVs using a custom agent from Microsoft Copilot Studio
2. **Matches** skills with staffing requirements
3. **Generates** standardized CVs via API in both PDF and DOCX formats
4. **Delivers** client-ready documents in under 5 minutes

---

## 🏗️ Architecture

```
┌─────────────────────────┐
│  Microsoft 365 Copilot  │
│   (Copilot Studio)      │
│                         │
│  • Extract CV data      │
│  • Generate JSON        │
└───────────┬─────────────┘
            │
            │ POST /generate-cv
            │ (JSON payload)
            ▼
┌─────────────────────────┐
│   FastAPI Backend       │
│   (Render/Azure)        │
│                         │
│  • Jinja2 templating    │
│  • LaTeX compilation    │
│  • PDF generation       │
│  • PDF → DOCX           │
└───────────┬─────────────┘
            │
            ▼
    📄 PDF + 📘 DOCX
            │
            ▼
┌─────────────────────────┐
│  Microsoft 365 Copilot  │
│   (Copilot Studio)      │
│                         │
│  • Retrieves the files  |
│and gives them to user   |
│                         │
└───────────┬─────────────┘
```

---

## 🚀 Features

- ✅ **M365 Integration**: Works directly within Microsoft Teams/Copilot
- ✅ **Dual Format Output**: PDF (professional) + DOCX (editable)
- ✅ **Standardized Layout**: Cluster Reply branding and formatting
- ✅ **Zero Manual Work**: Fully automated LaTeX compilation
- ✅ **JSON-based**: Structured data input/output

---

## 📂 Project Structure

```
cv-standardization-backend/
├── api.py                      # FastAPI application
├── main.py                     # Standalone test script
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment config
├── openapi.yaml               # API specification for Copilot Studio
├── template/
│   └── cv_template.tex        # LaTeX CV template (Jinja2)
└── assets/
    └── cluster_reply_logo.jpg # Company logo
```

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Templating**: Jinja2
- **Document Generation**: LaTeX (pdflatex/lualatex)
- **PDF → DOCX**: pdf2docx
- **Deployment**: Render.com (Free tier) or Azure Container Apps
- **AI Integration**: Microsoft Copilot Studio

---

## 📥 API Endpoints

### `POST /generate-cv`
Generate a CV from structured JSON data.

**Request Body:**
```json
{
  "id": "00001",
  "personal_info": {
    "full_name": "John Doe",
    "role": "Cloud Engineer",
    "department": "Consultant – Cloud Engineering",
    "email": "john.doe@example.com"
  },
  "summary": "Brief professional summary...",
  "key_achievements": ["Achievement 1", "Achievement 2"],
  "key_skills": [
    {
      "category": "Cloud Platforms",
      "items": ["Azure", "AWS", "Terraform"]
    }
  ],
  "certifications": [
    {"name": "AZ-104", "code": "AZ-104", "year": "2025"}
  ],
  "languages": [
    {"language": "English", "level": "Fluent"}
  ],
  "experience": [
    {
      "role": "Cloud Engineer",
      "company": "Cluster Reply GmbH",
      "start_date": "April 2025",
      "end_date": "Present",
      "description_list": ["Responsibility 1", "Responsibility 2"]
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "CV generated successfully",
  "pdf_path": "/path/to/cv.pdf",
  "docx_path": "/path/to/cv.docx"
}
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 🔧 Local Development

### Prerequisites
- Python 3.12+
- TeX Live (for LaTeX compilation)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/lorenzfiorellocluster/cv-standardization-backend.git
   cd cv-standardization-backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install TeX Live** (required for PDF generation)
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra

   # macOS
   brew install --cask mactex-no-gui
   ```

4. **Test the generator**
   ```bash
   python main.py
   ```
   This will generate test CV files in `output/`:
   - `cv_output.tex`
   - `cv_output.pdf`
   - `cv_output.docx`

5. **Run the API locally**
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```
   API available at: `http://localhost:8000`

---

## 🌐 Deployment

### Render.com (Current)
The API is deployed on Render.com free tier.

**Note**: Render Free tier has limitations with system package installation. For production, use Docker deployment or Azure Container Apps.

### Azure Container Apps (Recommended for Production)
Full Docker support with TeX Live included.

---

## 📝 Integration with Microsoft Copilot Studio

1. Upload `openapi.yaml` to Copilot Studio as a REST API tool
2. Configure the tool to call `POST /generate-cv`
3. The Copilot agent will automatically:
   - Extract CV information
   - Match skills with staffing requests
   - Call the API with structured JSON
   - Return generated CV files



## 👥 Authors

- **Lorenzo Fiorello** - Initial work and development

---


