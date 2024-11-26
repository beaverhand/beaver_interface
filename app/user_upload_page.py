import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from backend.task_queue import enqueue_resume_processing
# from utils.storage import save_uploaded_file


# Title and description
st.title("Resume Summarizer App")
st.write("Upload your resume and get a summary generated using our powerful language model. You can close the interface, and the process will continue in the backend.")

# File uploader
uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

# Directory to save uploaded files
UPLOAD_DIR = "..data/temp"

# if uploaded_file is not None:
#     # Save the uploaded file to the data/uploads directory
#     file_path = save_uploaded_file(uploaded_file, UPLOAD_DIR)
    
#     # Show a success message
#     st.success(f"Resume successfully uploaded! File saved at: {file_path}")
    
#     # Enqueue a task for processing the resume asynchronously
#     task_id = enqueue_resume_processing(file_path)
    
#     # Inform the user that the task is being processed
#     st.info(f"Your resume is being processed in the background. Task ID: {task_id}")
#     st.write("Feel free to close the application. You will be notified once the summary is ready.")

# # Footer message
# st.write("Powered by Streamlit, Celery, and LLM.")