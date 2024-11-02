This project is a **Resume Parser** application that extracts relevant information from resumes (PDF and Word formats) and stores it in a SQLite database. It utilizes Natural Language Processing (NLP) techniques to identify key elements such as email addresses, years of experience, and technical skills. The application features a web interface built with **Streamlit**, allowing users to search and rank resumes based on their specified criteria.

**Features**
- Extracts text from PDF and Word resume files.
- Parses resumes to extract emails, experience, and technical skills.
- Stores resume data in an SQLite database.
- Allows users to search for resumes based on minimum years of experience and required technical skills.
- Ranks resumes by matching skills using TF-IDF and cosine similarity.

## Files Overview
  
- **`test.py`**: Contains unit tests for various functionalities of the resume parser. It ensures that the extraction and storage processes work as intended.

- **`view_resume_table.py`**: This script provides a simple interface for viewing the contents of the `new_resumes.db` database. It allows users to query the database and see stored resume entries.

- **`new_resumes.db`**: The SQLite database file where extracted resume data is stored. It includes tables for resume entries with details such as filename, email, experience, technical skills, and a hash of the resume content.

- **`abcd/`**: This directory contains the resumes to be processed. The parser extracts information from PDF and Word documents stored in this folder.
