import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from io import StringIO
from backend.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    @patch('pandas.read_csv')
    def test_load_csv_with_resume_data(self, mock_read_csv):
        # Mock data to simulate CSV content
        mock_data = StringIO("Resume\nSample resume text\nAnother resume text")
        mock_read_csv.return_value = pd.read_csv(mock_data)

        # Instantiate the DataLoader and call the load_csv method
        df = DataLoader.load_csv("UpdatedResumeDataSet.csv")
        
        print(df.head())
        # Assert that 'Resume' column is in the DataFrame
        # self.assertIn("Resume", df.columns)
        # self.assertEqual(len(df), 2)  # Check number of rows
        # self.assertEqual(df['Resume'][0], "Sample resume text")  # Check specific data

if __name__ == '__main__':
    unittest.main()