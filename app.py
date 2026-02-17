import streamlit as st
import os
from ai_utils import extract_text_from_pdf, analyze_resume_with_ai, match_resume_to_job, rewrite_resume_for_job, generate_interview_questions

os.makedirs("resumes", exist_ok=True)



st.set_page_config(page_title="AI Job Hunter", layout="wide")
st.title("🤖 AI Autonomous Job Hunter")

# ---------- SESSION STATE ----------
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

# ---------- UPLOAD ----------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    save_path = os.path.join("resumes", uploaded_file.name)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state.resume_text = extract_text_from_pdf(save_path)
    st.success("Resume uploaded!")

# ---------- SHOW RESUME ----------
if st.session_state.resume_text:
    st.subheader("Resume Content")
    st.text_area("Extracted Text", st.session_state.resume_text, height=250)

# ---------- ANALYZE ----------
if st.button("Analyze Resume"):
    if st.session_state.resume_text:
        with st.spinner("Analyzing..."):
            st.session_state.analysis = analyze_resume_with_ai(st.session_state.resume_text)

# ---------- SHOW ANALYSIS ----------
if st.session_state.analysis:
    st.subheader("AI Resume Analysis")
    st.json(st.session_state.analysis)

# ---------- JOB DESCRIPTION ----------
if st.session_state.analysis:
    job_description = st.text_area("Paste Job Description")

    if st.button("Check Job Match"):
        with st.spinner("Evaluating..."):
            match = match_resume_to_job(st.session_state.analysis, job_description)
        st.subheader("Match Result")
        st.json(match)

    if st.button("Optimize My Resume"):
        with st.spinner("Optimizing resume..."):
            new_resume = rewrite_resume_for_job(st.session_state.resume_text, job_description)
        st.subheader("Optimized Resume")
        st.text_area("Improved Resume", new_resume, height=500)

# ---------- INTERVIEW PREPARATION ----------
if st.session_state.analysis:

    st.subheader("Prepare for Interview")

    if st.button("Generate Interview Questions"):
        if job_description.strip() == "":
            st.warning("Please paste the job description first.")
        else:
            with st.spinner("Preparing your interview training kit..."):
                questions = generate_interview_questions(job_description)

            st.subheader("Interview Preparation Guide")
            st.text_area("Your Interview Prep", questions, height=600)



# ---------- FOOTER ----------
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: gray;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>

    <div class="footer">
        Designed & Developed by <b>Benhail Benjamin</b>
    </div>
    """,
    unsafe_allow_html=True
)


