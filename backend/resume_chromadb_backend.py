import yaml
import os
import sys
import argparse
from backend.data_methods import DataLoader
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_community.llms import VLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

# def extract_text_from_pdfs(all_pdf_file_loc):
#     """
#     Extracts text from a list of PDF files.

#     Parameters:
#     all_pdf_file_loc (list): List of paths to PDF files to be summarized.

#     Returns:
#     list: A list of strings where each string is the extracted text from a PDF.
#     """
#     resume_text_list = []
#     for pdf_file_loc in all_pdf_file_loc:
#         resume_text = DataLoader.extract_text_from_pdf(pdf_file_loc)
#         resume_text_list.append(resume_text)
#     u_id_list = [int(x.split('.')[0].split('/')[-1]) for x in all_pdf_file_loc]
#     return resume_text_list, u_id_list

# def generate_summaries(resume_text_list, u_id_list, config):
#     """
#     Generates summaries of PDF resumes by running a language model on extracted text, 
#     and returning a list of user IDs, original texts, and their summaries.

#     Parameters:
#     all_pdf_file_loc (list): List of paths to PDF files to be summarized.
#     config (dict): Configuration dictionary containing model parameters, 
#                    LLM settings, and prompt template information.

#     Returns:
#     list: A list of tuples where each tuple contains (user_id, resume_text, report).
#     """

#     # Initialize LLM
#     llm = VLLM(
#         model=config['llm_model']['model'],
#         trust_remote_code=config['llm_model']['trust_remote_code'],
#         max_new_tokens=config['llm_model']['max_new_tokens'],
#         max_model_len=config['llm_model']['max_model_len'],
#         top_p=config['llm_model']['top_p'],
#         temperature=config['llm_model']['temperature'],
#         vllm_kwargs={"quantization": config['llm_model']['quantization']}
#     )

#     # Generate summaries
#     resume_summary_list = []
#     for resume_text in resume_text_list:
#         template = config['template']
#         prompt = PromptTemplate.from_template(template)
#         llm_chain = LLMChain(prompt=prompt, llm=llm)
#         resume_summary_list.append(llm_chain.invoke(resume_text)['text'])

#     return [(u_id, resume_text, summary) for u_id, resume_text, summary in 
#             zip(u_id_list,
#                 resume_text_list,
#                 resume_summary_list)]

# def split_resume_reports(resume_report_list, chunk_size=1000, chunk_overlap=100):
#     """
#     Splits the report text into smaller chunks for each user.

#     Args:
#     - resume_report_list (list of tuples): List of tuples in the format (u_id, resume_text, report).
#     - chunk_size (int): The size of each chunk.
#     - chunk_overlap (int): The overlap between chunks.

#     Returns:
#     - resume_report_split_list (list of tuples): List of tuples in the format 
#       (u_id, resume_text, split_chunks), where split_chunks is a list of split text chunks.
#     """
#     # Initialize RecursiveCharacterTextSplitter with given chunk_size and chunk_overlap
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
#     # List to store the split reports
#     resume_report_split_list = []

#     # Iterate over each tuple in the input list and split the report text
#     for u_id, resume_text, report in resume_report_list:
#         split_chunks = text_splitter.split_text(report)
#         resume_report_split_list.append((u_id, resume_text, split_chunks))

#     return resume_report_split_list

# def flatten_chunks_for_chromadb(resume_report_split_list):
#     """
#     Prepares the documents, metadata, and unique IDs for adding split reports to ChromaDB.

#     Args:
#     - resume_report_split_list (list of tuples): List of tuples in the format 
#       (u_id, resume_text, split_chunks), where split_chunks is a list of text chunks.

#     Returns:
#     - ids (list): List of unique IDs for each text chunk.
#     - documents (list): List of text chunks.
#     - metadata_list (list): List of metadata dictionaries containing user information.
#     """
#     # Initialize lists for documents, metadata, and ids
#     documents = []
#     metadata_list = []
#     ids = []

#     # Iterate over each tuple to extract chunks and prepare metadata
#     for u_id, resume_text, split_chunks in resume_report_split_list:
#         for idx, chunk in enumerate(split_chunks):
#             chunk_id = f"{u_id}_{idx}"  # Create a unique ID for each chunk

#             ids.append(chunk_id)
#             documents.append(chunk)
#             metadata_list.append({
#                 "user_id": u_id,
#                 "chunk_number": idx,
#                 "resume_text": [resume_text if idx == 0 else ''][0] 
#             })

#     return ids, documents, metadata_list

# def setup_chromadb_client(config):
#     """
#     Sets up a ChromaDB client and returns it.

#     Parameters:
#     config (dict): Configuration dictionary containing ChromaDB settings, including host and port.

#     Returns:
#     ChromaDB client object.
#     """
#     return chromadb.HttpClient(host=config['chromadb']['host'], port=config['chromadb']['port'])

# def setup_chromadb_collection(config, chroma_client):
#     """
#     Sets up a ChromaDB collection and returns it.

#     Parameters:
#     config (dict): Configuration dictionary containing ChromaDB settings, including model name and collection name.
#     chroma_client (ChromaDB client): ChromaDB client object.

#     Returns:
#     collection: ChromaDB collection object.
#     """
#     embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
#         model_name=config['chromadb']['model_name'],
#         trust_remote_code=config['chromadb']['trust_remote_code'],
#         # torch_dtype=torch.bfloat16 if config['chromadb'].get('use_bfloat16') else None
#     )
    
#     collection = chroma_client.get_or_create_collection(
#         name=config['chromadb']['collection_name'],
#         embedding_function=embedding_function,
#     )
    
#     return collection

# def add_documents_to_chromadb_collection(collection, ids, documents, metadatas):
#     """
#     Adds documents to a ChromaDB collection.

#     Parameters:
#     collection (ChromaDB collection): ChromaDB collection object.
#     ids (list): List of document IDs.
#     documents (list): List of document contents to be added to the ChromaDB collection.
#     metadata_list (list, optional): List of metadata dictionaries for the documents (default is None).
#     """
#     collection.add(
#         ids=ids,
#         documents=documents,
#         metadatas=metadatas
#     )

# def process_and_store_resumes(all_pdf_file_loc, config):
#     """
#     Processes PDF resumes, generates summaries, splits the summaries into chunks, 
#     and stores the chunks in a ChromaDB collection.

#     Parameters:
#     all_pdf_file_loc (list): List of paths to PDF files to be summarized.
#     config (dict): Configuration dictionary containing model parameters, LLM settings, 
#                    prompt template information, and ChromaDB settings.

#     Returns:
#     None
#     """

#     # Extract text and userID
#     resume_text_list, u_id_list = extract_text_from_pdfs(all_pdf_file_loc)
    
#     # Generate summaries
#     resume_report_list = generate_summaries(resume_text_list, u_id_list, config)

#     # Split resume reports into smaller chunks
#     nested_report_chunk_list = split_resume_reports(resume_report_list)

#     # Flatten chunks for ChromaDB
#     ids, documents, metadata_list = flatten_chunks_for_chromadb(nested_report_chunk_list)

#     # Setup ChromaDB client and collection
#     chroma_client = setup_chromadb_client(config)
#     collection = setup_chromadb_collection(config, chroma_client)

#     # Add documents to ChromaDB collection
#     add_documents_to_chromadb_collection(collection, ids, documents, metadata_list)

# def delete_collection(config):
#     client = setup_chromadb_client(config)
#     client.delete_collection(config['chromadb']['collection_name'])



class ResumeProcessorPipeline:
    def __init__(self, config):
        """
        Initializes the ResumeProcessor with the given configuration.

        Parameters:
        config (dict): Configuration dictionary containing model parameters, LLM settings, 
                       prompt template information, and ChromaDB settings.
        """
        self.config = config
        self.llm = None
        self.chroma_client = None
        self.collection = None

    def extract_text_from_pdfs(self, all_pdf_file_loc):
        """
        Extracts text from a list of PDF files.

        Parameters:
        all_pdf_file_loc (list): List of paths to PDF files to be summarized.

        Returns:
        list: A list of strings where each string is the extracted text from a PDF.
        """
        resume_text_list = []
        for pdf_file_loc in all_pdf_file_loc:
            resume_text = DataLoader.extract_text_from_pdf(pdf_file_loc)
            resume_text_list.append(resume_text)
        u_id_list = [int(x.split('.')[0].split('/')[-1]) for x in all_pdf_file_loc]
        return resume_text_list, u_id_list

    def generate_summaries(self, resume_text_list, u_id_list):
        """
        Generates summaries of PDF resumes by running a language model on extracted text.

        Parameters:
        resume_text_list (list): List of extracted resume texts.
        u_id_list (list): List of user IDs corresponding to each resume.

        Returns:
        list: A list of tuples where each tuple contains (user_id, resume_text, report).
        """
        if not self.llm:
            # Initialize LLM
            llm_config = self.config['llm_model']
            self.llm = VLLM(
                model=llm_config['model'],
                trust_remote_code=llm_config['trust_remote_code'],
                max_new_tokens=llm_config['max_new_tokens'],
                max_model_len=llm_config['max_model_len'],
                top_p=llm_config['top_p'],
                temperature=llm_config['temperature'],
                vllm_kwargs={"quantization": llm_config['quantization']}
            )

        # Generate summaries
        resume_summary_list = []
        for resume_text in resume_text_list:
            template = self.config['template']
            prompt = PromptTemplate.from_template(template)
            llm_chain = LLMChain(prompt=prompt, llm=self.llm)
            resume_summary_list.append(llm_chain.invoke(resume_text)['text'])

        return [(u_id, resume_text, summary) for u_id, resume_text, summary in 
                zip(u_id_list, resume_text_list, resume_summary_list)]

    def split_resume_reports(self, resume_report_list, chunk_size=1000, chunk_overlap=100):
        """
        Splits the report text into smaller chunks for each user.

        Args:
        - resume_report_list (list of tuples): List of tuples in the format (u_id, resume_text, report).
        - chunk_size (int): The size of each chunk.
        - chunk_overlap (int): The overlap between chunks.

        Returns:
        - List of tuples in the format (u_id, resume_text, split_chunks).
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        resume_report_split_list = []

        for u_id, resume_text, report in resume_report_list:
            split_chunks = text_splitter.split_text(report)
            resume_report_split_list.append((u_id, resume_text, split_chunks))

        return resume_report_split_list

    def flatten_chunks_for_chromadb(self, resume_report_split_list):
        """
        Prepares the documents, metadata, and unique IDs for adding split reports to ChromaDB.

        Args:
        - resume_report_split_list (list of tuples): List of tuples in the format 
          (u_id, resume_text, split_chunks).

        Returns:
        - ids (list): List of unique IDs for each text chunk.
        - documents (list): List of text chunks.
        - metadata_list (list): List of metadata dictionaries containing user information.
        """
        documents = []
        metadata_list = []
        ids = []

        for u_id, resume_text, split_chunks in resume_report_split_list:
            for idx, chunk in enumerate(split_chunks):
                chunk_id = f"{u_id}_{idx}"
                ids.append(chunk_id)
                documents.append(chunk)
                metadata_list.append({
                    "user_id": u_id,
                    "chunk_number": idx,
                    "resume_text": [resume_text if idx == 0 else ''][0]
                })

        return ids, documents, metadata_list

    def setup_chromadb(self):
        """
        Sets up a ChromaDB client and collection based on the configuration.
        """
        if not self.chroma_client:
            chromadb_config = self.config['chromadb']
            self.chroma_client = chromadb.HttpClient(host=chromadb_config['host'], port=chromadb_config['port'])

        if not self.collection:
            embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=chromadb_config['model_name'],
                trust_remote_code=chromadb_config['trust_remote_code']
            )
            self.collection = self.chroma_client.get_or_create_collection(
                name=chromadb_config['collection_name'],
                embedding_function=embedding_function,
            )

    def add_documents_to_chromadb_collection(self, ids, documents, metadatas):
        """
        Adds documents to a ChromaDB collection.
        """
        if not self.collection:
            raise ValueError("ChromaDB collection is not set up. Call setup_chromadb first.")
        self.collection.add(ids=ids, documents=documents, metadatas=metadatas)

    def process_and_store_resumes(self, all_pdf_file_loc):
        """
        Processes PDF resumes, generates summaries, splits the summaries into chunks, 
        and stores the chunks in a ChromaDB collection.
        """
        # Extract text and userID
        resume_text_list, u_id_list = self.extract_text_from_pdfs(all_pdf_file_loc)

        # Generate summaries
        resume_report_list = self.generate_summaries(resume_text_list, u_id_list)

        # Split resume reports into smaller chunks
        nested_report_chunk_list = self.split_resume_reports(resume_report_list)

        # Flatten chunks for ChromaDB
        ids, documents, metadata_list = self.flatten_chunks_for_chromadb(nested_report_chunk_list)

        # Setup ChromaDB client and collection
        self.setup_chromadb()

        # Add documents to ChromaDB collection
        self.add_documents_to_chromadb_collection(ids, documents, metadata_list)

    def delete_collection(self):
        """
        Deletes the ChromaDB collection specified in the config.
        """
        if not self.chroma_client:
            self.setup_chromadb()
        self.chroma_client.delete_collection(self.config['chromadb']['collection_name'])

    def query_top_candidates(self, query: str, n: int = 5) -> list:
        """
        Query the ChromaDB collection and retrieve the top N most similar candidates.

        Args:
            query (str): The query string to search for similar documents.
            n (int, optional): Number of top candidates to retrieve. Defaults to 5.

        Returns:
            list: A list of top N candidates, each containing document details.
        """
        try:
            # Perform the query on the collection
            results = self.collection.query(
                query_texts=[query],
                n_results=n
            )

            # Process and return the results
            candidates = []
            for i in range(len(results['ids'][0])):
                candidate = {
                    'id': results['ids'][0][i],
                    'document': results['documents'][0][i],
                    'distance': results['distances'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else None
                }
                candidates.append(candidate)

            return candidates

        except Exception as e:
            # Log the error or handle it as appropriate for your application
            print(f"Error querying ChromaDB: {e}")
            return []


if __name__ == '__main__':
    import yaml
    import os
    import sys
    import argparse

    # Adding the parent directory to the system path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "config.yaml")
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

    # Load configuration from config.yaml
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    pipeline = ResumeProcessorPipeline(config)
    all_pdf_file_loc = ['/home/roy/beaver_interface/data/temp/10189110.pdf']
    pipeline.process_and_store_resumes(all_pdf_file_loc)
    