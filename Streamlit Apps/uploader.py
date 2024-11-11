import chromadb
from PyPDF2 import PdfReader
import streamlit as st

# Initialize ChromaDB client
client = chromadb.HttpClient(host='localhost', port=8000)

# Define a collection for resumes
collection_name = "resumes"
if collection_name not in [col.name for col in client.list_collections()]:
    collection = client.create_collection(collection_name)
else:
    collection = client.get_collection(collection_name)

# Function to parse PDF text
def parse_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

    

# Function to add resume to ChromaDB
def add_resume_to_db(file, candidate_name):
    text = parse_pdf(file)
    # Create a unique ID for each resume entry
    doc_id = candidate_name.replace(" ", "_").lower()
    collection.add  (documents=[text], metadatas=[{"name": candidate_name}], ids=[doc_id])
    return f"Resume for {candidate_name} added to ChromaDB."

# Streamlit interface
st.title("Resume Uploader for ChromaDB")

# Input for candidate name
candidate_name = st.text_input("Candidate Name")

# File uploader for resume (PDF)
uploaded_file = st.file_uploader("Upload Resume (PDF format only)", type=["pdf"])

# Submit button
if st.button("Upload and Save Resume"):
    if uploaded_file and candidate_name:
        # Ingest the resume into ChromaDB
        result = add_resume_to_db(uploaded_file, candidate_name)
        st.success(result)
    else:
        st.error("Please provide a candidate name and upload a PDF resume.")