import pandas as pd

class DataLoader:
    def load_csv(file_path):
        df = pd.read_csv(file_path)
        if 'UpdatedResumeDataSet' in file_path:
            df = df[['Resume']]
        return df