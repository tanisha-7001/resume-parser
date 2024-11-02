This project is a **Resume Parser** application that extracts relevant information from resumes (PDF and Word formats) and stores it in a SQLite database. It utilizes Natural Language Processing (NLP) techniques to identify key elements such as email addresses, years of experience, and technical skills. The application features a web interface built with **Streamlit**, allowing users to search and rank resumes based on their specified criteria.

**Features**
- Extracts text from PDF and Word resume files.
- Parses resumes to extract emails, experience, and technical skills.
- Stores resume data in an SQLite database.
- Allows users to search for resumes based on minimum years of experience and required technical skills.
- Ranks resumes by matching skills using TF-IDF and cosine similarity.
