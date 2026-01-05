from helper import create_embeddings
from prompt import system_prompt
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate  
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_ollama import OllamaLLM                             # OllamaLLM for using ollama models by downloading locally
from config import settings
from dotenv import load_dotenv
load_dotenv()

PINECONE_API_KEY=settings.PINECONE_API_KEY
HUGGINGFACEHUB_API_TOKEN=settings.HUGGINGFACE_API_KEY
PINECONE_ENVIRONMENT=settings.PINECONE_ENV

embeddings = create_embeddings()

index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever =  docsearch.as_retriever(search_type = "similarity", search_kwargs = {"k":3})


prompt = PromptTemplate(
    input_variables=["input","context"],
    template=system_prompt
)

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    max_new_tokens=512,
    temperature=0.7,
)

model = ChatHuggingFace(llm=llm)

# model = OllamaLLM(                            Optional: Using Ollama LLM instead of HuggingFace
#     model="llama3",
#     temperature=0.3
# )

question_answer_chain = create_stuff_documents_chain(model, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

