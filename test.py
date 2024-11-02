import os
import sqlite3
import PyPDF2
import re
import docx
import streamlit as st
import hashlib
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# load the spacy model
nlp = spacy.load("en_core_web_sm")

# list of technical skills 
technical_skills = ["python", "javascript", "sql", "html", "css", "machine learning", 
                    "data analysis", "react", "docker", "kubernetes"]

def init_db():
    conn = sqlite3.connect("new_resumes.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS resumes
                 (id INTEGER PRIMARY KEY, filename TEXT, email TEXT, experience INTEGER, 
                  tech_skills TEXT, resume_hash TEXT)''')
    conn.commit()
    conn.close()

#hash resume content
def hash_resume_content(text):
    return hashlib.md5(text.encode()).hexdigest()

# Store resume data in the db
def store_resume_data(filename, email, experience, tech_skills):
    conn = sqlite3.connect("new_resumes.db")
    c = conn.cursor()
    resume_hash = hash_resume_content(tech_skills)
    c.execute("SELECT COUNT(*) FROM resumes WHERE filename = ? OR resume_hash = ?", 
              (filename, resume_hash))
    exists = c.fetchone()[0]
    if exists == 0:
        c.execute("INSERT INTO resumes (filename, email, experience, tech_skills, resume_hash) VALUES (?, ?, ?, ?, ?)",
                  (filename, email, experience, tech_skills, resume_hash))
        conn.commit()
    conn.close()

# retrieve resumes based on   experience and skills
def retrieve_resumes(min_experience):
    conn = sqlite3.connect("new_resumes.db")
    c = conn.cursor()
    query = "SELECT * FROM resumes WHERE experience >= ?"
    c.execute(query, (min_experience,))
    resumes = c.fetchall()
    conn.close()
    return resumes

# Function to extract text from pdf
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''.join(page.extract_text() for page in reader.pages)
    return text

# Extract text from word documents
def extract_text_from_word(docx_path):
    doc = docx.Document(docx_path)
    return '\n'.join(paragraph.text for paragraph in doc.paragraphs)

# parse resume text and extract  relevant information
def parse_resume(text):
    doc = nlp(text)
    email = None
    experience_years = 0
    tech_skills = []

    # Extracting   email
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = email_pattern.findall(text)
    if emails:
        email = emails[0]

    # Extract experience and skills
    for ent in doc.ents:
        if ent.label_ == "DATE":
            try:
                experience_years = max(experience_years, int(ent.text.split()[0]))
            except (ValueError, IndexError):
                pass
        elif ent.label_ == "ORG" or ent.label_ == "PRODUCT":
            tech_skills.append(ent.text.lower())

    # lemmatize skills to match against technical skills list{specified at  beginning of the code}
    keywords = [token.lemma_ for skill in tech_skills for token in nlp(skill)]
    keywords = list(set(skill for skill in keywords if skill in technical_skills))
    keywords_str = ', '.join(keywords)

    return email, experience_years, keywords_str

init_db()

# Streamlit UI
st.title("Resume Parser")
st.sidebar.title("Filter Resumes")
input_experience = st.sidebar.number_input("Minimum Years of Experience", min_value=0, max_value=50, value=2)
input_skills = st.sidebar.multiselect("Select Required Skills", technical_skills)

# Search  button 
if st.sidebar.button("Search Resumes"):
    st.write("Matching Resumes")
    resumes = retrieve_resumes(input_experience)
    
    if resumes:
        resume_texts = [resume[4] for resume in resumes]  #resume[4] is tech_skills column in the database
        resume_filenames = [resume[1] for resume in resumes]  #  resume[1] stores filename

        skills_text = ' '.join(input_skills)

        # TF-IDF vectorization and similarity calculation
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(resume_texts + [skills_text])
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]

        # Rank resumes 
        ranked_resumes = sorted(zip(resume_filenames, resumes, similarity_scores), key=lambda x: x[2], reverse=True)

        # Display
        for idx, (filename, resume, score) in enumerate(ranked_resumes):
            st.subheader(f"{idx + 1}: {filename}")
            st.write(f"Email: {resume[2]}")
            st.write(f"Experience: {resume[3]} years")
            st.write(f"Skills: {resume[4]}")
            
            #download link for the resume file
            file_path = os.path.join("C:/Users/Tanisha Singh/Desktop/resume/abcd", filename)
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    st.download_button(label=f"Download {filename}", data=file, file_name=filename)
    else:
        st.write("No resumes match the selected criteria.")
else:
    # Parse resumes from abcd folder and store in the database
    folder_path = "C:/Users/Tanisha Singh/Desktop/resume/abcd"
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file_name.endswith(".docx"):
            text = extract_text_from_word(file_path)
        else:
            continue
        email, experience, tech_skills = parse_resume(text)
        store_resume_data(file_name, email, experience, tech_skills)
    st.write("Resumes have been processed and stored in the database.")
