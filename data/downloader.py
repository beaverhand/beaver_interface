from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
model.save('/home/roy/beaver_interface/data/embedding_model')