import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from backend.task_queue import enqueue_resume_processing
from backend.data_methods import DataLoader


# Title and description
st.title("BEAVERHAND")
st.write("Upload your resume here to help us know you better!")

# File uploader
uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

# Directory to save uploaded files
UPLOAD_DIR = "data/temp"

if uploaded_file is not None:
    # Save the uploaded file to the data/uploads directory
    file_path = DataLoader.save_uploaded_pdf(uploaded_file, UPLOAD_DIR)
    
    # Show a success message
    st.success(f"Resume successfully uploaded!")
    
    # # Enqueue a task for processing the resume asynchronously
    # task_id = enqueue_resume_processing(file_path)
    
    # # Inform the user that the task is being processed
    # st.info(f"Your resume is being processed in the background. Task ID: {task_id}")
    # st.write("Feel free to close the application. You will be notified once the summary is ready.")

# Footer message
st.write("Powered by beaverhand!!!")