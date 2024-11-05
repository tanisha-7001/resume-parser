## Resume Parsing Application
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

## Requirements
-Install dependencies using:  
```python
pip install os sqlite3 PyPDF2 re docx streamlit hashlib spacy scikit-learn
```

## Path Configuration

1. **Resume Folder Path (`resume_folder_path`)**:
   - Update the `folder_path` variable to the path where your `.pdf` and `.docx` resumes are stored.
   - Example in code:
     ```python
     folder_path = "C:/Users/Tanisha Singh/Desktop/resume/abcd"  # Update this to user's path
     ```

2. **Download Path for Streamlit**:
   - Update the `file_path` used for generating download links in Streamlit to the folder where your resumes are located.
   - Example in code:
     ```python
     file_path = os.path.join("C:/Users/Tanisha Singh/Desktop/resume/abcd", filename)  # Update this to user's path
     ```


## Run the Streamlit App:
```python
 streamlit run test.py
```
OR
```python
python -m streamlit run test.py
```

## View Database Contents: 
To view the stored resume data in new_resumes.db, run the following command:
```python
streamlit run view_resume_table.py
```
OR  
```python
python -m streamlit run view_resume_table.py
```








