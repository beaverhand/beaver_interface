from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_resume_reports(resume_report_list, chunk_size=1000, chunk_overlap=100):
    """
    Splits the report text into smaller chunks for each user.

    Args:
    - resume_report_list (list of tuples): List of tuples in the format (u_id, resume_text, report).
    - chunk_size (int): The size of each chunk.
    - chunk_overlap (int): The overlap between chunks.

    Returns:
    - resume_report_split_list (list of tuples): List of tuples in the format 
      (u_id, resume_text, split_chunks), where split_chunks is a list of split text chunks.
    """
    # Initialize RecursiveCharacterTextSplitter with given chunk_size and chunk_overlap
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    # List to store the split reports
    resume_report_split_list = []

    # Iterate over each tuple in the input list and split the report text
    for u_id, resume_text, report in resume_report_list:
        split_chunks = text_splitter.split_text(report)
        resume_report_split_list.append((u_id, resume_text, split_chunks))

    return resume_report_split_list

def flatten_chunks_for_chromadb(resume_report_split_list):
    """
    Prepares the documents, metadata, and unique IDs for adding split reports to ChromaDB.

    Args:
    - resume_report_split_list (list of tuples): List of tuples in the format 
      (u_id, resume_text, split_chunks), where split_chunks is a list of text chunks.

    Returns:
    - ids (list): List of unique IDs for each text chunk.
    - documents (list): List of text chunks.
    - metadata_list (list): List of metadata dictionaries containing user information.
    """
    # Initialize lists for documents, metadata, and ids
    documents = []
    metadata_list = []
    ids = []

    # Iterate over each tuple to extract chunks and prepare metadata
    for u_id, resume_text, split_chunks in resume_report_split_list:
        for idx, chunk in enumerate(split_chunks):
            chunk_id = f"{u_id}_{idx}"  # Create a unique ID for each chunk

            ids.append(chunk_id)
            documents.append(chunk)
            metadata_list.append({
                "user_id": u_id,
                "chunk_number": idx,
                "resume_text": [resume_text if idx == 1 else 0] 
            })

    return ids, documents, metadata_list
