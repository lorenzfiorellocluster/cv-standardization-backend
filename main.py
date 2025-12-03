import os
from jinja2 import Environment, FileSystemLoader
from docx import Document

# -------------------------------------------------------
# JSON DI TEST INSERITO DIRETTAMENTE NEL CODICE
# -------------------------------------------------------
cv = {
    "id": "00001",
    "personal_info": {
        "full_name": "John Doe",
        "role": "Cloud Engineering Consultant",
        "department": "Consultant – Cloud Engineering",
        "seniority": "Senior",
        "location": "Berlin, Germany",
        "email": "john.doe@example.com",
        "phone": "+49 151 12345678"
    },

    "summary": "Cloud Engineering Consultant with hands-on experience on Azure, AWS, Terraform and DevOps automation.",
    "key_achievements": [
        "30% faster deployments through CI/CD optimization",
        "35% reduction in code review time via AI-powered tooling",
        "30% cost optimization on cloud workloads",
        "90% faster environment provisioning with Terraform modules"
    ],

    "key_skills": [
        {
            "category": "Cloud Platforms",
            "items": [
                "Azure (2 yrs): AKS, App Services, Storage, VNets",
                "AWS (1.5 yrs): EC2, Lambda, RDS, CloudWatch"
            ]
        },
        {
            "category": "Programming & Scripting",
            "items": [
                "PowerShell (2 yrs)",
                "Python",
                "Bash",
                "YAML",
                "JSON"
            ]
        },
        {
            "category": "Infrastructure as Code",
            "items": [
                "Terraform (2 yrs)",
                "Bicep",
                "CloudFormation"
            ]
        },
        {
            "category": "Containers & Orchestration",
            "items": [
                "Docker (2 yrs)",
                "Kubernetes/AKS",
                "Azure Container Apps"
            ]
        }
    ],

    "certifications": [
        { "name": "Azure Administrator", "code": "AZ-104", "year": "2025" },
        { "name": "Terraform Associate", "code": "003", "year": "2025" },
        { "name": "Solutions Architect", "code": "SAA-C03", "year": "2024" }
    ],

    "languages": [
        { "language": "German", "level": "Native" },
        { "language": "English", "level": "Fluent (C2)" }
    ],

    "experience": [
        {
            "role": "Cloud Engineer",
            "company": "Cluster Reply GmbH",
            "start_date": "April 2025",
            "end_date": "Present",
            "description_list": [
                "Cloud engineering, IaC automation, DevOps",
                "Speaker at Developer Summit Berlin 2025: AI Security & Workflows"
            ]
        }
    ],

    "relevant_skills_for_request": [
        {
            "skill": "Terraform",
            "confidence": "0.95",
            "quote_from_cv": "experience with Terraform modules"
        }
    ]
}

# -------------------------------------------------------
# ADD LOGO PATH FOR LATEX
# -------------------------------------------------------
cv["logo_path"] = "../assets/cluster_reply_logo.jpg"

# -------------------------------------------------------
# RENDER LATEX
# -------------------------------------------------------
TEMPLATE_DIR = "template"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    block_start_string="{%",
    block_end_string="%}",
    variable_start_string="{{",
    variable_end_string="}}",
    comment_start_string="{#",
    comment_end_string="#}"
)

template = env.get_template("cv_template.tex")
latex_output = template.render(cv)

tex_path = os.path.join(OUTPUT_DIR, "cv_output.tex")
with open(tex_path, "w", encoding="utf-8") as f:
    f.write(latex_output)

print("✔ Generated LaTeX:", tex_path)

# -------------------------------------------------------
# GENERATE SIMPLE DOCX VERSION
# -------------------------------------------------------
doc = Document()
doc.add_heading(cv["personal_info"]["full_name"], level=1)
doc.add_paragraph(cv["summary"])

doc.add_heading("Key Achievements", level=2)
for ach in cv["key_achievements"]:
    doc.add_paragraph(f"- {ach}")

doc_path = os.path.join(OUTPUT_DIR, "cv_output.docx")
doc.save(doc_path)

print("✔ Generated DOCX:", doc_path)
