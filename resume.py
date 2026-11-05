import io,re
def extract_text(data,name):
 if name.lower().endswith(".pdf"):
  from pypdf import PdfReader
  return "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages)
 if name.lower().endswith(".docx"):
  from docx import Document
  return "\n".join(p.text for p in Document(io.BytesIO(data)).paragraphs)
 return data.decode("utf-8",errors="ignore")
def extract_skills(t):
 known=["Java","Spring Boot","Spring MVC","SQL","MySQL","SQL Server","REST APIs","Angular","JavaScript","HTML","CSS","C#",".NET","ASP.NET Core","Python","AWS","Azure","Docker","Kubernetes","Terraform","Jenkins","Ansible","Linux","Git","Prometheus","Grafana","SonarQube","Trivy","OWASP ZAP","Microservices","Hibernate","Postman","CI/CD","Data Analysis","Communication"]
 return [s for s in known if re.search(re.escape(s),t,re.I)]
