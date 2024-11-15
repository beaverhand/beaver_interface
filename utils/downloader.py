import yaml
from sentence_transformers import SentenceTransformer

with open("../config.yaml", "r") as file:
    config = yaml.safe_load(file)
model = SentenceTransformer(config['embedding_model']['name'])
model.save(config['embedding_model']['path'])