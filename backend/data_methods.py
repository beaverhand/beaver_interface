import pandas as pd
import re
import os

class DataLoader:
    def save_uploaded_pdf(uploaded_file, directory):
            # if not os.path.exists(directory):
            #     os.makedirs(directory)
            file_path = os.path.join(directory, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return file_path
    def extract_text_from_pdf(file_path):
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text