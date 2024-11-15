import streamlit as st
from backend.resume_parser import parse_resumes_from_drive
from backend.embedding_generator import generate_embeddings
from backend.db_handler import add_embeddings_to_db

def bulk_loader_page():
    st.title("Bulk Loader")
    folder_id = st.text_input("Enter Google Drive Folder ID:")
    if st.button("Upload Resumes"):
        with st.spinner("Processing resumes..."):
            resumes = parse_resumes_from_drive(folder_id)
            embeddings = generate_embeddings(resumes)
            add_embeddings_to_db(embeddings)
            st.success("Resumes uploaded and processed successfully!")