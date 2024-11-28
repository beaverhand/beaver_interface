import yaml
import os
import sys
import argparse

# Adding the parent directory to the system path
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "..", "config.yaml")
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

# Import the processing function from backend.resume_chromadb_backend
from backend.resume_chromadb_backend import process_and_store_resumes


# Load configuration from config.yaml
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

# Define the command-line argument parser
parser = argparse.ArgumentParser(description="Process and store resumes in ChromaDB")
parser.add_argument('--files', '-f', metavar='F', type=str, nargs='+',
                    help='Path(s) to the PDF file(s) to be processed')

# Parse the command-line arguments
args = parser.parse_args()

# Get the list of file paths from the arguments
all_pdf_file_loc = args.files

# Call the function with the file paths and configuration
if all_pdf_file_loc:
    process_and_store_resumes(all_pdf_file_loc, config)
else:
    print("No file paths provided. Please specify the PDF file paths using the --files or -f flag.")

