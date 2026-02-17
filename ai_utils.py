import os
import json
from dotenv import load_dotenv
from pypdf import PdfReader
from openai import OpenAI

# Load API key
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------- PDF READER ----------------
def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"

    return text


# ---------------- RESUME ANALYSIS ----------------
def analyze_resume_with_ai(resume_text):

    prompt = f"""
You are an AI recruiter assistant.

Analyze the following resume and extract structured information.

Return ONLY valid JSON.

Required JSON format:
{{
  "candidate_name": "",
  "skills": [],
  "tools": [],
  "programming_languages": [],
  "projects": [],
  "probable_role": ""
}}

Resume:
{resume_text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a professional technical recruiter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    result = response.choices[0].message.content

    # Clean JSON
    cleaned = result.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        cleaned = cleaned.replace("json", "", 1).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}") + 1
    cleaned = cleaned[start:end]

    return json.loads(cleaned)


# ---------------- JOB MATCHING ----------------
def match_resume_to_job(resume_analysis, job_description):

    prompt = f"""
You are an AI hiring evaluator.

Evaluate how well the candidate matches the job.

Return ONLY JSON.

Format:
{{
  "match_score": 0,
  "matched_skills": [],
  "missing_skills": [],
  "final_verdict": ""
}}

Candidate Profile:
{resume_analysis}

Job Description:
{job_description}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a strict technical recruiter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    result = response.choices[0].message.content

    cleaned = result.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        cleaned = cleaned.replace("json", "", 1).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}") + 1
    cleaned = cleaned[start:end]

    return json.loads(cleaned)


# ---------------- RESUME OPTIMIZER ----------------
def rewrite_resume_for_job(resume_text, job_description):

    prompt = f"""
You are an expert technical resume writer and ATS optimizer.

Rewrite the candidate's resume to better match the provided job description.

Rules:
- Do NOT invent fake experience
- Improve bullet points
- Add relevant technical keywords
- ATS friendly
- Professional tone

Return clean formatted resume text.

Resume:
{resume_text}

Job Description:
{job_description}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a professional resume optimization expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


# ---------------- INTERVIEW COACH ----------------
def generate_interview_questions(job_description):

    prompt = f"""
You are a senior technical interviewer.

Based on the following job description, prepare interview questions for the candidate.

Return clear sections:

1) Technical Questions (with sample answers)
2) HR Questions (with suggested answers)
3) Topics the candidate must study before interview

Job Description:
{job_description}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an experienced software engineering interviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content

