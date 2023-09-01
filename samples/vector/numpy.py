import numpy as np
from sentence_transformers import SentenceTransformer

text_to_embed = "The quick brown fox jumps over the lazy dog"

# Choose the model that works best
model = SentenceTransformer('sentence-transformers/all-distilroberta-v1')

# 
embedding = model.encode(text_to_embed).astype(np.float32).tobytes()
