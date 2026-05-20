import streamlit as st
import pickle
import pdfplumber
import re
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ---------------- CLEAN TEXT ----------------

def clean_text(text):
    text = re.sub(r'http\\S+', '', text)
    text = re.sub(r'[^A-Za-z ]', '', text)
    text = text.lower()
    return text

# ---------------- EXTRACT TEXT ----------------

def extract_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text

# ---------------- SIDEBAR ----------------

st.sidebar.title("📌 About Project")

st.sidebar.info(
    """
    AI-powered Resume Screening System

    Features:
    ✅ Resume Category Prediction
    ✅ Skill Extraction
    ✅ ATS Resume Score
    ✅ Missing Skills Detection
    ✅ Skill Match Percentage
    ✅ PDF Resume Upload
    """
)

st.sidebar.write("Built using:")
st.sidebar.write("- Python")
st.sidebar.write("- Machine Learning")
st.sidebar.write("- NLP")
st.sidebar.write("- Streamlit")

# ---------------- TITLE ----------------

st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>
    📄 AI Resume Screening System
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align: center; font-size:18px;'>
    Upload your resume and let AI analyze it instantly 🚀
    </p>
    """,
    unsafe_allow_html=True
)

st.write("---")

# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "📤 Upload Resume PDF",
    type=["pdf"]
)

# ---------------- MAIN LOGIC ----------------

if uploaded_file is not None:

    with st.spinner("Analyzing Resume..."):

        # Extract text
        resume_text = extract_text(uploaded_file)

        # Clean text
        cleaned_resume = clean_text(resume_text)

        # Vectorize
        resume_vector = vectorizer.transform([cleaned_resume])

        # Predict
        prediction = model.predict(resume_vector)

    st.success("✅ Resume Analysis Completed")

    # ---------------- RESULT SECTION ----------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🎯 Predicted Job Category")

        st.info(prediction[0])

    # ---------------- SKILLS ----------------

    skills = [
        "python",
        "sql",
        "machine learning",
        "deep learning",
        "excel",
        "power bi",
        "tableau",
        "java",
        "html",
        "css",
        "javascript",
        "communication",
        "data analysis",
        "react",
        "mongodb",
        "nodejs",
        "streamlit",
        "nlp",
        "tensorflow",
        "pandas"
    ]

    found_skills = []

    for skill in skills:
        if skill in cleaned_resume:
            found_skills.append(skill)

    with col2:

        st.subheader("🛠 Skills Found")

        if found_skills:

            for skill in found_skills:

                st.markdown(
                    f"""
                    <span style="
                    background-color:#4CAF50;
                    padding:8px;
                    border-radius:10px;
                    color:white;
                    margin:5px;
                    display:inline-block;
                    ">
                    {skill}
                    </span>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.warning("No matching skills found")

    st.write("---")

    # ---------------- MATCH PERCENTAGE ----------------

    st.subheader("📊 Skill Match Percentage")

    required_skills = len(skills)

    match_percentage = (
        len(found_skills) / required_skills
    ) * 100

    st.progress(int(match_percentage))

    st.write(f"### {match_percentage:.2f}% Match")

    # ---------------- ATS SCORE ----------------

    st.write("---")

    st.subheader("📄 ATS Resume Score")

    ats_score = min(
        int(match_percentage + 20),
        100
    )

    st.metric(
        label="ATS Score",
        value=f"{ats_score}/100"
    )

    # ---------------- MISSING SKILLS ----------------

    st.write("---")

    st.subheader("❌ Missing Skills")

    missing_skills = []

    for skill in skills:
        if skill not in found_skills:
            missing_skills.append(skill)

    if missing_skills:

        for skill in missing_skills[:8]:

            st.markdown(
                f"""
                <span style="
                background-color:#FF4B4B;
                padding:8px;
                border-radius:10px;
                color:white;
                margin:5px;
                display:inline-block;
                ">
                {skill}
                </span>
                """,
                unsafe_allow_html=True
            )

    # ---------------- PIE CHART ----------------

    st.write("---")

    st.subheader("📈 Resume Analysis Chart")

    labels = [
        "Matched Skills",
        "Missing Skills"
    ]

    values = [
        len(found_skills),
        len(missing_skills)
    ]

    fig, ax = plt.subplots()

    ax.pie(
        values,
        labels=labels,
        autopct='%1.1f%%'
    )

    st.pyplot(fig)

    # ---------------- RESUME TEXT ----------------

    st.write("---")

    with st.expander("📄 View Extracted Resume Text"):

        st.write(resume_text[:3000])

# ---------------- FOOTER ----------------

st.write("---")

st.markdown(
    """
    <center>
    Developed with ❤️ using Machine Learning & NLP
    </center>
    """,
    unsafe_allow_html=True
)