import streamlit as st
import spacy
from PyPDF2 import PdfReader
from io import BytesIO
import base64
import os

# Load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="AI Resume Evaluator", layout="wide")

# Sidebar
with st.sidebar:
    st.header("📝 Resume Evaluator")
    st.markdown("""
    **Instructions:**
    1. Upload your Resume (PDF)
    2. Paste the Job Description
    3. Get an AI-based match score and feedback
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

# Main title
st.title("💼 AI-Powered Resume Evaluator")

# File uploader
uploaded_file = st.file_uploader("📤 Upload your Resume (PDF only)", type=["pdf"])

# Job Description input
job_description = st.text_area("💼 Paste the Job Description Here", height=200)

if uploaded_file and job_description:
    # Resume Preview Section
    st.subheader("📄 Resume Preview")
    pdf_reader = PdfReader(uploaded_file)
    resume_text = ""
    for page in pdf_reader.pages:
        resume_text += page.extract_text()
    st.text_area("Resume Text", resume_text, height=300)

    # Process both texts
    resume_doc = nlp(resume_text.lower())
    jd_doc = nlp(job_description.lower())

    # Matching keywords and computing score
    resume_tokens = set([token.text for token in resume_doc if token.is_alpha])
    jd_tokens = set([token.text for token in jd_doc if token.is_alpha])

    matched_keywords = resume_tokens.intersection(jd_tokens)
    match_score = round(len(matched_keywords) / len(jd_tokens) * 100, 2) if jd_tokens else 0

    st.subheader("📊 Evaluation Result")
    st.markdown(f"### ✅ Skill Match Score: {match_score}%")

    st.progress(match_score / 100)

    st.markdown("### 🔍 Matched Keywords")
    st.write(", ".join(sorted(matched_keywords)) if matched_keywords else "No matches found.")

    # Option to download the result
    result_text = f"Skill Match Score: {match_score}%\n\nMatched Keywords:\n" + ", ".join(matched_keywords)
    result_bytes = BytesIO(result_text.encode())
    st.download_button("📥 Download Evaluation Result", result_bytes, file_name="resume_evaluation.txt")

else:
    st.info("Please upload your resume and paste the job description to proceed.")
