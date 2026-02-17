import streamlit as st
import os
from ai_utils import extract_text_from_pdf, analyze_resume_with_ai, match_resume_to_job, rewrite_resume_for_job, generate_interview_questions

os.makedirs("resumes", exist_ok=True)

st.set_page_config(page_title="AI Job Hunter", layout="wide")
st.markdown("""
<style>

/* Main container padding */
.block-container {
    padding-top: 2rem;
}

/* Buttons */
.stButton>button {
    border-radius: 10px;
    height: 3em;
    font-weight: 600;
    background: linear-gradient(90deg, #6366F1, #4F46E5);
    color: white;
}

/* Text area */
textarea {
    border-radius: 10px !important;
}

/* File uploader */
section[data-testid="stFileUploader"] {
    border: 1px dashed #4F46E5;
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align: center;'>🤖 AI Job Hunter</h1>
<h4 style='text-align: center; color: gray;'>
An AI assistant that analyzes resumes, matches jobs, optimizes CVs, and prepares interviews
</h4>
""", unsafe_allow_html=True)

st.divider()

# ---------- SESSION STATE ----------
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

# ---------- LAYOUT ----------
left_col, right_col = st.columns(2)

# ---------- LEFT: RESUME ----------
with left_col:
    st.subheader("📄 Resume Upload")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded_file is not None:
        save_path = os.path.join("resumes", uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state.resume_text = extract_text_from_pdf(save_path)
        st.success("Resume uploaded!")

    if st.session_state.resume_text:
        st.text_area("Extracted Resume", st.session_state.resume_text, height=300)

    if st.button("Analyze Resume", key="analyze_btn"):
        if st.session_state.resume_text:
            with st.spinner("Analyzing candidate profile..."):
                st.session_state.analysis = analyze_resume_with_ai(st.session_state.resume_text)

    if st.session_state.analysis:
        st.subheader("Candidate Profile")
        st.json(st.session_state.analysis)

# ---------- RIGHT: JOB MATCH ----------
with right_col:
    if st.session_state.analysis:
        st.subheader("💼 Job Matching")

        st.session_state.job_description = st.text_area(
            "Paste Job Description",
            value=st.session_state.job_description,
            height=300
        )

        if st.button("Check Job Match", key="match_btn"):
            with st.spinner("Evaluating job compatibility..."):
                match = match_resume_to_job(st.session_state.analysis, st.session_state.job_description)

            st.subheader("Match Result")
            st.json(match)

# ---------- TOOLS ----------
if st.session_state.analysis:

    tab1, tab2 = st.tabs(["🧠 Resume Optimizer", "🎯 Interview Coach"])

    with tab1:
        if st.button("Optimize My Resume", key="optimize_btn"):
            if st.session_state.job_description.strip() == "":
                st.warning("Please paste the job description first.")
            else:
                with st.spinner("Optimizing resume..."):
                    new_resume = rewrite_resume_for_job(
                        st.session_state.resume_text,
                        st.session_state.job_description
                    )
                st.text_area("Optimized Resume", new_resume, height=500)

    with tab2:
        if st.button("Generate Interview Questions", key="interview_btn"):
            if st.session_state.job_description.strip() == "":
                st.warning("Please paste the job description first.")
            else:
                with st.spinner("Preparing interview kit..."):
                    questions = generate_interview_questions(st.session_state.job_description)
                st.text_area("Interview Preparation", questions, height=600)

# ---------- FOOTER ----------
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
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
