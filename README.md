AI Autonomous Job Hunter 🤖


An end-to-end AI-powered job application assistant that helps candidates analyze resumes, evaluate job fit, optimize resumes for ATS systems, and prepare for interviews using Large Language Models.

Live Capabilities

This system simulates how modern companies screen candidates automatically.

The application can:

• Parse resumes directly from PDF
• Extract skills and candidate profile using LLM reasoning
• Compare candidate profile with job descriptions
• Calculate job match score
• Identify missing skills
• Optimize resume for ATS compatibility
• Generate interview preparation questions and answers

Tech Stack

Python
Streamlit
OpenAI API (LLM reasoning)
Prompt Engineering
PDF Parsing (pypdf)
JSON structured output handling

Features

1. Resume Analyzer
Uploads a resume and extracts:
skills
tools
programming languages
projects
probable role

3. Job Matching Engine
   
Compares resume against a job description and returns:
match score
matched skills
missing skills
final hiring verdict


4. Resume Optimizer
Rewrites resume bullet points to improve ATS compatibility while keeping information truthful.

6. Interview Coach
   
Generates:

technical interview questions
HR questions
suggested answers
topics to study before interview
How to Run Locally
git clone https://github.com/Benhail06/ai-job-hunter.git
cd ai-job-hunter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
Create a .env file and add:
OPENAI_API_KEY=your_api_key_here

Project Purpose

This project demonstrates how LLMs can be used to automate real-world workflows beyond chatbots by building a multi-step reasoning pipeline for job applications and candidate evaluation.

Author

Benhail Benjamin
