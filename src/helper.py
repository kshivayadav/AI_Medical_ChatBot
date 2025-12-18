from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
import torch


def load_pdf_files(file_path):
    loader = DirectoryLoader(file_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

def filter_documents(docs:List[Document]) -> List[Document]:
    """Given a list of documents, return a new list of Document objects
    containing only 'source' in metadata and the original page content.
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        minimal_docs.append(Document(page_content=doc.page_content, metadata={"source": doc.metadata.get("source")}))
    return minimal_docs


def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    chunks = text_splitter.split_documents(minimal_docs)
    return chunks



def create_embeddings():
    """Create HuggingFace embeddings with device configuration."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"})
    return embeddings