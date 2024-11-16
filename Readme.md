# Resume Dataset Chroma DB and RAG Implementation

This is an implementation of RAG tool 

## Introduction

The repository provides tools and instructions for creating a Chroma database to store and retrieve information effectively. By implementing RAG, the system enhances information search and ranking, aiming to generate accurate responses to complex queries based on data stored within ChromaDB. This project leverages PyTorch, Streamlit, and several other libraries to facilitate seamless interaction between Chroma DB and RAG.

## Dataset Link: 
https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset

## Reference Links

- **Chroma DB Creation**: [YouTube Tutorial](https://www.youtube.com/watch?v=61kaK-e3Owc)
- **RAG Implementation**:
  - **Information Search and Rank Paper**: [OpenReview Paper](https://openreview.net/pdf?id=vhLAb1dpIw)
  - **RAG General Implementation**: [GitHub Repository](https://github.com/GURPREETKAURJETHRA/RAG-using-Llama3-Langchain-and-ChromaDB)
  - **RAG Specific Implementation**: [Kaggle Notebook](https://www.kaggle.com/code/gpreda/rag-using-llama3-langchain-and-chromadb)

## Architecture Detail

This document will outline the step-by-step architecture for integrating Chroma DB and RAG.

### Step 1

- Details to be provided in the final architecture document.

## Frequently Required Commands

Use the following commands for setting up your environment and running essential components:

### Docker Command for ChromaDB

```bash
docker run -p 8000:8000 -v /home/roy/chromadb:/chroma/chroma chromadb/chroma
conda create -n resume_chromadb_env python=3.9
conda install -c conda-forge streamlit -y
conda install -c conda-forge chromadb -y
conda install -c conda-forge pypdf2 -y
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y

```



## Data Creation 

```bash
unzip resume-dataset.zip -d /home/roy/beaver_interface/data/temp_resume_dataset
mkdir -p /home/roy/beaver_interface/data/Resume
find /home/roy/beaver_interface/data/temp_resume_dataset -type f -name "*.pdf" -exec mv {} /home/roy/beaver_interface/data/Resume \;
rm -rf /home/roy/beaver_interface/data/temp_resume_dataset


kaggle datasets download madhab/jobposts -p /home/roy/beaver_interface/data/Job_description --unzip
```


## Misc
[Miro](https://miro.com/app/board/uXjVLEHfhy4=/)