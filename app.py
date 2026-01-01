from backend.src.config import settings
from flask import Flask, render_template, jsonify, request
from backend.src.helper import create_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from backend.src.prompt import system_prompt
import os

app = Flask(__name__)




PINECONE_API_KEY=settings.PINECONE_API_KEY
HUGGINGFACEHUB_API_TOKEN=settings.HUGGINGFACE_API_KEY
PINECONE_ENVIRONMENT=settings.PINECONE_ENV

print(PINECONE_API_KEY)
print(PINECONE_ENVIRONMENT)
print(HUGGINGFACEHUB_API_TOKEN)



embeddings = create_embeddings()

index_name = "medical-chatbot"
# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)




retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})


llm = HuggingFaceEndpoint(
        repo_id='openai/gpt-oss-120b',
        task='text-generation',
        temperature=0.7,
    )
chatModel = ChatHuggingFace(llm=llm)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)



@app.route("/")
def index():
    return render_template('chat.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response["answer"])
    return str(response["answer"])



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)









