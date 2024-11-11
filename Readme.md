Chroma DB creation: https://www.youtube.com/watch?v=61kaK-e3Owc
command-- docker run -p 8000:8000 -v /home/roy/chroma:/chroma/chroma chromadb/chroma

conda create -n resume_chromadb_env python=3.9

conda install -c conda-forge streamlit -y
conda install -c conda-forge chromadb -y
conda install -c conda-forge pypdf2 -y


