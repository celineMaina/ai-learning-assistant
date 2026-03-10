import os
import tempfile
from pathlib import Path
import numpy as np

from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

#from pptx import Presentation

# Temporarily change CWD so ChromaDB's pydantic-settings does not pick up
# the project .env file (which contains DB_URL, an unknown key for ChromaDB).
_orig_cwd = os.getcwd()
os.chdir(tempfile.gettempdir())
import chromadb
os.chdir(_orig_cwd)


# Configure path to files
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project root
KNOWLEDGE_BASE = BASE_DIR / "app" / "knowledge_base" / "cirriculum"
CHROMADB_PATH = BASE_DIR / "app" / "chroma_db"

# Model configuration
MODEL_NAME = 'BAAI/bge-small-en-v1.5'
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

embedding_model = SentenceTransformer(MODEL_NAME)

# Normalize vectors
def normalize_embeddings(embeddings):
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return (embeddings / norms).tolist()

# Read different file types (pdf, md, pptx, txt etc)
def extract_pdf(path):
    reader = PdfReader(path)
    text = " "

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text
    
def extract_markdown(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# def extract_pptx(path):
    # prs = Presentation(path)
    # text = " "

    # for slide in prs.slides:
        # for shape in slide.shapes:
            # if hasattr(shape, "text"):
                # text += shape.text + "\n"

def extract_text(file_path):
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return extract_pdf(file_path)
    
    elif suffix == ".md":
        return extract_markdown(file_path)
    
    # elif suffix == ".pptx":
        # return extract_pptx(file_path)
    
    else:
        print(f"Unsupported file: {file_path.name}")
        return ""
    
def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


# Chunking
def chunk_text(text, size=500, overlap=50):
    words = text.split()
    chunks = []
    step = size - overlap

    for i in range(0, len(words), step):
        chunks.append(" ".join(words[i:i + size]))

    return chunks
    

# Vector db
client = chromadb.PersistentClient(path=str(CHROMADB_PATH))

collection = client.get_or_create_collection(
    name="knowledge_base",
    metadata={"description" : "DSA course knowledge base"}
)

all_chunks = []
all_embeddings = []
all_ids = []
all_metadata = []

doc_id_counter = 0

# Iterate through the knowledge base to read all the documents
for file_path in KNOWLEDGE_BASE.iterdir():
     if not file_path.is_file():
         continue
     
     print(f"Processing: {file_path.name}")

     text = extract_text(file_path)

     if not text:
         continue
     
     text = clean_text(text)
     chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
     
     embeddings = embedding_model.encode(chunks)
     embeddings = normalize_embeddings(embeddings)

     for i, chunk in enumerate(chunks):
          all_chunks.append(chunk)
          all_embeddings.append(embeddings[i])
          all_ids.append(f"doc_{doc_id_counter}")
          all_metadata.append({"source": file_path.name})
          doc_id_counter += 1


# Store everything in the vector db
collection.add(
    documents=all_chunks,
    embeddings=all_embeddings,
    ids=all_ids,
    metadatas=all_metadata
)

print("Documents stored successfully!")