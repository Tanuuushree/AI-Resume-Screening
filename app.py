import streamlit as st
import pickle
import pdfplumber
import re

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Resume Screening & Job Matching System",
    page_icon="📄",
    layout="wide"
)

# ---------------- LOAD MODEL ---------------- #

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1 {
    color: #8BE78B;
    text-align: center;
    font-size: 45px;
}

.stTextArea textarea {
    background-color: #262730;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #161A23;
}

.skill-box {
    background-color: #1E88E5;
    padding: 8px 14px;
    border-radius: 10px;
    color: white;
    margin: 5px;
    display: inline-block;
    font-size: 14px;
}

.match-box {
    background-color: #1F2937;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📌 About Project")

st.sidebar.info("""
### AI Resume Screening & Job Matching System

This AI-powered application helps:

✅ Resume Category Prediction  
✅ Skill Extraction  
✅ Resume-Job Matching  
✅ ATS Score Analysis  
✅ Eligibility Checking  
✅ Missing Skill Recommendation  
✅ Recruiter AI Feedback  

Built using:
- Python
- Machine Learning
- NLP
- Streamlit
""")

# ---------------- TITLE ---------------- #

st.title("📄 AI Resume Screening & Job Matching System")

st.markdown(
    "<h4 style='text-align:center;'>Analyze resumes intelligently using AI & ATS 🚀</h4>",
    unsafe_allow_html=True
)

st.write("---")

# ---------------- JOB DESCRIPTION FIRST ---------------- #

st.subheader("🏢 Recruiter Job Requirements")

job_description = st.text_area(
    "Paste Job Description / Required Skills",
    height=220,
    placeholder="""
Example:

Python
Machine Learning
SQL
NLP
Streamlit
Communication
GitHub
"""
)

# ---------------- RESUME UPLOAD ---------------- #

st.write("---")

st.subheader("📄 Candidate Resume")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# ---------------- SKILLS LIST ---------------- #

skills = [

    # Programming
    "python",
    "java",
    "c",
    "c++",
    "javascript",

    # Web
    "html",
    "css",
    "react",
    "nodejs",
    "flask",
    "django",
    "streamlit",

    # AI / Data
    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "pytorch",
    "data science",
    "data analysis",

    # Database
    "sql",
    "mysql",
    "mongodb",

    # Tools
    "excel",
    "power bi",
    "git",
    "github",

    # Soft Skills
    "communication",
    "leadership",
    "problem solving",
    "teamwork",

    # Cloud
    "aws",
    "azure",
    "devops"
]

# ---------------- PROCESS RESUME ---------------- #

if uploaded_file is not None:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            extracted_text = page.extract_text()

            if extracted_text:

                text += extracted_text

    # ---------------- CLEAN TEXT ---------------- #

    cleaned_resume = re.sub(r"[^a-zA-Z ]", " ", text)
    cleaned_resume = cleaned_resume.lower()

    # ---------------- SMART CATEGORY PREDICTION ---------------- #

    if (
        "machine learning" in cleaned_resume
        or "deep learning" in cleaned_resume
        or "nlp" in cleaned_resume
        or "tensorflow" in cleaned_resume
    ):

        predicted_category = "AI / ML Engineer"

    elif (
        "python" in cleaned_resume
        or "flask" in cleaned_resume
        or "django" in cleaned_resume
    ):

        predicted_category = "Python Developer"

    elif (
        "html" in cleaned_resume
        or "css" in cleaned_resume
        or "javascript" in cleaned_resume
    ):

        predicted_category = "Web Developer"

    elif (
        "sql" in cleaned_resume
        or "power bi" in cleaned_resume
        or "excel" in cleaned_resume
    ):

        predicted_category = "Data Analyst"

    else:

        predicted_category = "Software Engineer"

    # ---------------- SKILLS FOUND ---------------- #

    found_skills = []

    for skill in skills:

        if skill.lower() in cleaned_resume:

            found_skills.append(skill)

    # ---------------- REQUIRED SKILLS ---------------- #

    required_skills = []

    if job_description:

        required_skills = [
            skill for skill in skills
            if skill.lower() in job_description.lower()
        ]

    # ---------------- MATCH PERCENTAGE ---------------- #

    if required_skills:

        matched_required_skills = [
            skill for skill in required_skills
            if skill in found_skills
        ]

        match_percentage = (
            len(matched_required_skills)
            / len(required_skills)
        ) * 100

    else:

        match_percentage = 0

    # ---------------- MISSING SKILLS ---------------- #

    missing_skills = list(
        set(required_skills) - set(found_skills)
    )

    # ---------------- CATEGORY ---------------- #

    st.write("---")

    st.subheader("🎯 Predicted Resume Category")

    st.success(predicted_category)

    # ---------------- FOUND SKILLS ---------------- #

    st.write("---")

    st.subheader("🛠 Skills Found In Resume")

    if found_skills:

        for skill in found_skills:

            st.markdown(
                f'<div class="skill-box">{skill}</div>',
                unsafe_allow_html=True
            )

    else:

        st.warning("No skills detected")

    # ---------------- REQUIRED SKILLS ---------------- #

    st.write("---")

    st.subheader("📌 Required Skills")

    if required_skills:

        for skill in required_skills:

            st.markdown(
                f'<div class="skill-box">{skill}</div>',
                unsafe_allow_html=True
            )

    else:

        st.warning("No job description provided")

    # ---------------- RECOMMENDED SKILLS ---------------- #

    st.write("---")

    st.subheader("📚 Recommended Skills To Learn")

    if missing_skills:

        for skill in missing_skills:

            st.markdown(
                f'<div class="skill-box">{skill}</div>',
                unsafe_allow_html=True
            )

    else:

        st.success("Excellent! No missing skills")

    # ---------------- ATS SCORE ---------------- #

    st.write("---")

    st.subheader("📊 ATS Resume Match Score")

    st.progress(int(match_percentage))

    st.markdown(
        f"""
        <div class="match-box">
        <h1>{match_percentage:.2f}%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- RESUME STRENGTH ---------------- #

    st.subheader("💡 Resume Strength")

    if match_percentage >= 80:

        st.success("Excellent Resume 🚀")

    elif match_percentage >= 60:

        st.info("Good Resume 👍")

    elif match_percentage >= 40:

        st.warning("Average Resume ⚠️")

    else:

        st.error("Weak Resume ❌")

    # ---------------- ELIGIBILITY ---------------- #

    if match_percentage >= 70:

        st.success("✅ Eligible For This Role")

    elif match_percentage >= 40:

        st.warning("⚠️ Partially Eligible - Improve Some Skills")

    else:

        st.error("❌ Not Eligible - Need More Skills")

    # ---------------- RECRUITER FEEDBACK ---------------- #

    st.write("---")

    st.subheader("🧠 Recruiter AI Feedback")

    if match_percentage >= 80:

        st.success("""
Candidate has strong technical skills matching the job requirements.
Highly recommended for interview.
""")

    elif match_percentage >= 60:

        st.info("""
Candidate matches many required skills.
Can be considered for interview round.
""")

    else:

        st.warning("""
Candidate needs improvement in technical skills
to match this role effectively.
""")

# ---------------- FOOTER ---------------- #

st.write("---")

st.markdown(
    "<h5 style='text-align:center;'>Developed with ❤️ using Machine Learning & NLP</h5>",
    unsafe_allow_html=True
)