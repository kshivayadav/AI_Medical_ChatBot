from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Settings:
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
    HUGGINGFACE_API_KEY = os.environ["HUGGINGFACEHUB_API_TOKEN"]
    PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

settings = Settings()
