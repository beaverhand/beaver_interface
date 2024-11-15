import pandas as pd
import re

class DataLoader:
    def load_csv(file_path):
        try: 
            df = pd.read_csv(file_path)
            if 'UpdatedResumeDataSet' in file_path:
                df = df[['Resume']]
            return df
        
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")


class DataCleaner:
    def clean_resume_text(text):
        # # Remove emails
        # text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', '', text)
        # # Remove phone numbers (matches different international formats)
        # text = re.sub(r'\b(\+?\d{1,3})?[-. ]?(\(?\d{2,4}\)?)?[-. ]?\d{2,4}[-. ]?\d{2,4}[-. ]?\d{2,9}\b', '', text)
        # # Remove URLs
        # text = re.sub(r'http\S+|www\.\S+', '', text)
        # # Remove unwanted characters (e.g., non-alphanumeric symbols except common punctuation)
        # text = re.sub(r'[^A-Za-z0-9.,;:\s]', '', text)
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text).strip()
        # # Remove common resume words (if needed)
        # text = re.sub(r'\b(Resume|Curriculum Vitae|CV|Profile|Experience|Education|Skills|References)\b', '', text, flags=re.IGNORECASE)
        return text