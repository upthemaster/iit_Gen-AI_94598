import streamlit as st
from resume_handler import ResumeManager
from vector_db import VectorStoreManager
from rag import RAGEngine

st.set_page_config(page_title="Resume Shortlisting Assistant", layout="wide")

resume_mgr = ResumeManager()
vector_mgr = VectorStoreManager()
rag_engine = RAGEngine(vector_mgr)

st.title("Resume Shortlisting Assistant")

menu = st.sidebar.selectbox(
    "Choose Action",
    ["Upload Resume", "List Resumes", "Delete Resume", "Shortlist Resumes"]
)

# Upload Resume
if menu == "Upload Resume":
    file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    if file:
        path = resume_mgr.save_resume(file)
        vector_mgr.add_resume(path)
        st.success("Resume uploaded successfully")

# List of Resumes
elif menu == "List Resumes":
    resumes = resume_mgr.list_resumes()
    if resumes:
        st.write(resumes)
    else:
        st.info("No resumes found")

# Delete Resume
elif menu == "Delete Resume":
    resumes = resume_mgr.list_resumes()
    selected = st.selectbox("Select Resume", resumes)
    if st.button("Delete"):
        resume_mgr.delete_resume(selected)
        vector_mgr.delete_resume_vectors(selected)
        st.success("Resume and embeddings deleted")

# Shortlist Resume
elif menu == "Shortlist Resumes":
    jd = st.text_area("Enter Job Description...")
    top_n = st.number_input("No. of resumes to shortlist", min_value=1, value=3)

    if st.button("Shortlist"):
        results = rag_engine.shortlist_resumes(jd, top_n)
        st.subheader("Shortlisted Resumes :)")
        for r in results:
            st.write(r)
