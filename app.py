# app.py

import streamlit as st
import pickle
import pdfplumber
import re

# Load model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Clean text
def clean_text(text):
    text = re.sub(r'http\\S+', '', text)
    text = re.sub(r'[^A-Za-z ]', '', text)
    text = text.lower()
    return text

# Extract text from PDF
def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Streamlit UI
st.title("AI Resume Screening System")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    # Extract text
    resume_text = extract_text(uploaded_file)

    # Clean resume text
    cleaned_resume = clean_text(resume_text)

    # Convert text into vector
    resume_vector = vectorizer.transform([cleaned_resume])

    # Predict category
    prediction = model.predict(resume_vector)

    # Display prediction
    st.success(f"Predicted Job Category: {prediction[0]}")

    # Skills list
    skills = [
        "python",
        "sql",
        "machine learning",
        "excel",
        "power bi",
        "tableau",
        "java",
        "html",
        "css",
        "javascript",
        "c"
    ]

    # Find matching skills
    found_skills = []

    for skill in skills:
        if skill in cleaned_resume:
            found_skills.append(skill)

    # Display skills
    st.subheader("Skills Found")

    if found_skills:
        st.write(found_skills)
    else:
        st.write("No matching skills found")

    # Match percentage
    required_skills = len(skills)

    match_percentage = (
        len(found_skills) / required_skills
    ) * 100

    # Display match percentage
    st.subheader("Skill Match Percentage")

    st.write(f"{match_percentage:.2f}%")