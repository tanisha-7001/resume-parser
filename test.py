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
import numpy as np

#loading the spacy model 
nlp = spacy.load("en_core_web_sm")

# list of technical skills
technical_skills = ["python", "javascript", "sql", "html", "css", "machine learning", "data analysis", "react", "docker", "kubernetes"]

# Initialize database
def init_db():
    conn = sqlite3.connect("new_resumes.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS resumes
                 (id INTEGER PRIMARY KEY, filename TEXT, email TEXT, experience INTEGER, tech_skills TEXT, resume_hash TEXT)''')
    conn.commit()
    conn.close()

#hash resume content
def hash_resume_content(text):
    return hashlib.md5(text.encode()).hexdigest()

def store_resume_data(filename, email, experience, tech_skills, resume_text):
    conn = sqlite3.connect("new_resumes.db")
    c = conn.cursor()
    resume_hash = hash_resume_content(resume_text)
    c.execute("SELECT COUNT(*) FROM resumes WHERE filename = ? OR resume_hash = ?", (filename, resume_hash))
    exists = c.fetchone()[0]
    if exists == 0:
        c.execute("INSERT INTO resumes (filename, email, experience, tech_skills, resume_hash) VALUES (?, ?, ?, ?, ?)",
                  (filename, email, experience, tech_skills, resume_hash))
        conn.commit()
    conn.close()

def retrieve_resumes(min_experience, skills):
    conn = sqlite3.connect("new_resumes.db")
    c = conn.cursor()
    query = "SELECT * FROM resumes WHERE experience >= ?"
    params = [min_experience]
    c.execute(query, params)
    resumes = c.fetchall()
    conn.close()
    return resumes

# Resume parsing functions for pdf
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''.join(page.extract_text() for page in reader.pages)
    return text
#resume parsing function for word files
def extract_text_from_word(docx_path):
    doc = docx.Document(docx_path)
    return '\n'.join(paragraph.text for paragraph in doc.paragraphs)

#NER to extract skills, experience, etc.
def parse_resume(text):
    doc = nlp(text)
    email = None
    experience_years = 0
    tech_skills = []

    # Extract email 
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = email_pattern.findall(text)
    if emails:
        email = emails[0]  

    # using NER   to identify entities and lemmatize
    for ent in doc.ents:
        if ent.label_ == "DATE":  
            try:
                experience_years = max(experience_years, int(ent.text.split()[0]))
            except (ValueError, IndexError):
                pass
        elif ent.label_ == "ORG" or ent.label_ == "PRODUCT":  
            tech_skills.append(ent.text.lower())

    # Lemmatize tech skills
    tech_skills = [token.lemma_ for skill in tech_skills for token in nlp(skill)]
    tech_skills = list(set(skill for skill in tech_skills if skill in technical_skills))
    tech_skills_str = ', '.join(tech_skills)

    # Lemmatize the resume text l
    lemmatized_text = ' '.join(token.lemma_ for token in doc)

    return email, experience_years, tech_skills_str, lemmatized_text

# Initialize   database
init_db()

#  Streamlit UI
st.title("Resume Parser and Database Integration with TF-IDF Ranking")
st.sidebar.title("Filter Resumes")
input_experience = st.sidebar.number_input("Minimum Years of Experience", min_value=0, max_value=50, value=2)
input_skills = st.sidebar.multiselect("Select Required Skills", technical_skills)

# Search resumes button
if st.sidebar.button("Search Resumes"):
    st.write("Matching Resumes (Ranked by Skill Match)")
    resumes = retrieve_resumes(input_experience, input_skills)
    
    if resumes:
        # Extract text descriptions of skills for TF-IDF vectorization
        resume_texts = [resume[4] for resume in resumes]  # resume[4] is tech_skills column
        resume_filenames = [resume[1] for resume in resumes]  # Resue[1] stores filename
 
        skills_text = ' '.join(input_skills)

        # TF-IDF vectorization
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(resume_texts + [skills_text])
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]

        #rank resumes by score
        ranked_resumes = sorted(zip(resume_filenames, resumes, similarity_scores), key=lambda x: x[2], reverse=True)
        
        # Display
        for idx, (filename, resume, score) in enumerate(ranked_resumes):
            st.subheader(f"{idx + 1}: {filename}")
            st.write(f"Email: {resume[2]}")
            st.write(f"Experience: {resume[3]} years")
            st.write(f"Skills: {resume[4]}")
            
            # file path for downloads
            file_path = os.path.join("C:/Users/Tanisha Singh/Desktop/resume/abcd", filename)
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    st.download_button(label=f"Download {filename}", data=file, file_name=filename)
    else:
        st.write("No resumes match the selected criteria.")
else:
    #parse resumes from a folder and store in the db
    folder_path = "C:/Users/Tanisha Singh/Desktop/resume/abcd"
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file_name.endswith(".docx"):
            text = extract_text_from_word(file_path)
        else:
            continue
        email, experience, tech_skills, resume_text = parse_resume(text)
        store_resume_data(file_name, email, experience, tech_skills, resume_text)
    st.write("Resumes have been processed and stored in the database.")
