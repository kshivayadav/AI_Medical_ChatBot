from fastapi import FastAPI
from rag_pipeline import rag_chain
from schema import ChatRequest,ChatResponse


app = FastAPI(title = "Medical Chatbot API", version = "1.0")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical Chatbot API"}


@app.get("/health")
def health_check():
    return {"Status": "ok",
            "version": "1.0",
            "message":"Medical Chatbot API is Running Successfully"}

@app.post("/medicalchatbot",response_model = ChatResponse)
def medical_chatbot(query:ChatRequest):
    response = rag_chain.invoke({"input": query.question})
    print(response)
    return ChatResponse(
        answer = response['answer']
    )


