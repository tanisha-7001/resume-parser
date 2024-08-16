import re
from pdfminer.high_level import extract_text

def parse_resume(path):
    text = extract_text(path)
    lines = text.split('\n')
    #email 
    for line in lines:
        match = re.search("\S+@\S+.\S+",line)
        if match:
            email = match.group()
            break

    #skills 
    keywords = ['Python', 'JavaScript', 'React', 'Node.js', 'Java', 'C++', 'SQL', 'HTML',
     'CSS', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP']
    skills = []
    for k in keywords:
        if k in text:
            skills.append(k)

    #name
    for line in lines[:5]:
        if line.strip():
            name = line.strip()
            break
    
    print("Name:", name)
    print("Email:", email)
    print("Tech Skills:", ', '.join(skills))

path = "C:/Users/Tanisha Singh/Desktop/resume/sample.pdf"
parse_resume(path)
