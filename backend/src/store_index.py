from config import settings
import os
from helper import load_pdf_files,filter_documents,text_split,create_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

PINECONE_API_KEY = settings.PINECONE_API_KEY

if not PINECONE_API_KEY:
    raise ValueError("❌ PINECONE_API_KEY not found in environment variables")

print(PINECONE_API_KEY)  # safe debug

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATA_DIR = os.path.join(BASE_DIR, "Data")
print("Loading PDFs from:", DATA_DIR)

extracted_docs = load_pdf_files(file_path = DATA_DIR)
minimal_docs = filter_documents(extracted_docs)
text_chunks = text_split(minimal_docs)

embeddings = create_embeddings()

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"
if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension = 384,
        metric = "cosine",
        spec = ServerlessSpec(cloud ="aws", region = settings.PINECONE_ENV)
    )
index = pc.Index(index_name)

docsearch = PineconeVectorStore.from_documents(
    documents = text_chunks,
    embedding = embeddings,
    index_name = index_name
)



