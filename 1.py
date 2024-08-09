import re
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def parse_resume(text):
    lines = text.split('\n')
    
    name = None
    for line in lines[:5]: 
        if line.strip():
            name = line.strip()
            break
    
    phone = None
    phone_pattern = re.compile(r'\b(?:\+?(\d{1,3})?[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\d{10})\b')
    for line in lines:
        match = phone_pattern.search(line)
        if match:
            phone = match.group()
            break
    
    email = None
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    for line in lines:
        match = email_pattern.search(line)
        if match:
            email = match.group()
            break
    
    print("Name:", name)
    print("Phone:", phone)
    print("Email:", email)

if __name__ == "__main__":
    pdf_path = "C:/Users/Tanisha Singh/Desktop/resume/Tanisha Singh Resume.pdf"
    text = extract_text_from_pdf(pdf_path)
    if text:
        parse_resume(text)
