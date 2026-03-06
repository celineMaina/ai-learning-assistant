import os
from sentence_transformers import SentenceTransformer
import chromadb


embedding_model = SentenceTransformer('BAAI/bge-small-en-v1.5')

