import streamlit as st
import sqlite3
import pandas as pd

def display():
    conn = sqlite3.connect("new_resumes.db")
    df = pd.read_sql_query("SELECT * FROM resumes", conn)
    conn.close()
    return df

st.write("Resume DB View")
st.dataframe(display())
