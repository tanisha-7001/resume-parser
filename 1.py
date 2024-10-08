import re
from pdfminer.high_level import extract_text

def parse_resume(path, job_title):
    text = extract_text(path)
    lines = text.split('\n')
    
    #  email
    email = None
    for line in lines:
        match = re.search(r"\S+@\S+\.\S+", line)
        if match:
            email = match.group()
            break

    # skills
    keywords = ['Python','Maven','Jenkins','Oracle', 'JavaScript', 'React', 'Node.js', 'Java', 'C++', 'SQL', 'HTML',
                'CSS', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP']
    skills = [k for k in keywords if k in text]

    # name 
    name = None
    for line in lines[:5]:
        if line.strip():
            name = line.strip()
            break

    # LinkedIn 
    linkedin = None
    for line in lines:
        match = re.search(r'linkedin\.com/\S+', line, re.IGNORECASE)
        if match:
            linkedin = match.group()
            break
    
    # years of experience
    yoe = None
    yoe_pattern = r'(\d+)\s*(years|yrs)'
    for line in lines:
        match = re.search(yoe_pattern, line, re.IGNORECASE)
        if match:
            yoe = match.group(1) + ' years'
            break

    # title 
    job= 'Yes' if re.search(rf'\b{job_title}\b', text, re.IGNORECASE) else 'No'

    print("Name:", name)
    print("Email:", email)
    print("LinkedIn:", linkedin)
    print("Tech Skills:", ', '.join(skills))
    print("Years of Experience:", yoe)
    print(f"Job Title ({job_title}):", job)

path = "Sachin-Sangle.pdf"
job_title = "Project Manager" 
parse_resume(path, job_title)
