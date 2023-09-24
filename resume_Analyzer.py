import streamlit as st
import PyPDF2
import spacy
import requests  # To make API requests

# Load spaCy's English NLP model
nlp = spacy.load("en_core_web_sm")

# LinkedIn API credentials
LINKEDIN_API_KEY = "YOUR_LINKEDIN_API_KEY"  # Replace with your LinkedIn API key
HEADERS = {"Authorization": f"Bearer {LINKEDIN_API_KEY}"}

# Function to extract text from PDF (as shown in your previous code)
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        # Use PyPDF2 to read text from the uploaded PDF file
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    except Exception as e:
        st.error(f"Error parsing PDF: {e}")
    
    return text

# Function to analyze the resume (as shown in your previous code)
def analyze_resume(resume_text):

    doc = nlp(resume_text)

    # Extract entities (e.g., education, skills, work experience) using spaCy's named entity recognition
    education = []
    skills = []
    work_experience = []

    for ent in doc.ents:
        if ent.label_ == "EDUCATION":
            education.append(ent.text)
        elif ent.label_ == "SKILL":
            skills.append(ent.text)
        elif ent.label_ == "WORK_EXPERIENCE":
            work_experience.append(ent.text)

    return education, skills, work_experience
# Function to get job recommendations from LinkedIn API
def get_job_recommendations(skills, work_experience):
    query = " ".join(skills + work_experience)
    URL = f"https://api.linkedin.com/v2/jobSearch?keywords={query}&count=5"
    response = requests.get(URL, headers=HEADERS)

    if response.status_code == 200:
        job_recommendations = response.json()
        return job_recommendations.get("elements", [])
    else:
        st.error("Failed to fetch job recommendations from LinkedIn API.")
        return []

def main():
    st.title("Resume Analysis App")

    st.header("Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a resume (PDF)", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Analyze Resume"):
            resume_text = extract_text_from_pdf(uploaded_file)

            # Analyze the resume
            education, skills, work_experience = analyze_resume(resume_text)

            st.subheader("Education:")
            st.write(education)

            st.subheader("Skills:")
            st.write(skills)

            st.subheader("Work Experience:")
            st.write(work_experience)

            st.subheader("Job Recommendations:")
            job_recommendations = get_job_recommendations(skills, work_experience)
            for recommendation in job_recommendations:
                st.write(recommendation.get("title", ""))
                st.write(recommendation.get("companyName", ""))
                st.write(recommendation.get("locationName", ""))
                st.write("")

if __name__ == "__main__":
    main()