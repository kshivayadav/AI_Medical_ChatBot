# 🏥 AI Medical Chatbot (RAG-Based)

An **AI-powered Medical Chatbot** built using **FastAPI, LangChain, Pinecone, and Streamlit**, designed to provide **accurate, context-aware medical information** by leveraging **Retrieval-Augmented Generation (RAG)**.

---

## 🚀 Project Overview

The AI Medical Chatbot allows users to ask medical-related questions and receive **reliable answers grounded in medical documents**.  
Instead of generating answers purely from a language model, this system **retrieves relevant medical knowledge** and then generates responses based on that context.

---

## 🧠 Key Features

- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Context-aware medical responses
- ✅ FastAPI backend (async & scalable)
- ✅ Streamlit-based interactive frontend
- ✅ Pinecone vector database for semantic search
- ✅ Industry-level logging & middleware
- ✅ Clean UI with chat bubbles (User vs Bot)
- ✅ Error handling and validation
- ⚠️ Educational use only (not medical advice)

---

## 🏗️ Tech Stack

### Backend
- **FastAPI** – High-performance REST API
- **LangChain** – RAG pipeline orchestration
- **Pinecone** – Vector database for embeddings
- **HuggingFace / Ollama** – LLM inference
- **Sentence Transformers** – Text embeddings
- **Pydantic** – Data validation

### Frontend
- **Streamlit** – Interactive UI

### Other Tools
- Python 3.10+
- Uvicorn
- dotenv
- PDF loaders

---

## 📁 Project Structure
```bash
AI_Medical_ChatBot/
│
├── backend/
│ ├── src/
│ │ ├── main.py # FastAPI entry point
│ │ ├── rag_pipeline.py # RAG chain logic
│ │ ├── helper.py # PDF loading & embeddings
│ │ ├── store_index.py # Pinecone index creation
│ │ ├── schema.py # Request & response models
│ │ ├── prompt.py # prompt for instructions
│ │ ├── config.py # configuring the variables
│ │ ├── __init__.py
│ │ ├── requirements.txt 
├── Data/
│ └── Medical_book.pdf # Medical knowledge source
│
├── frontend/
│ └── app.py # Streamlit UI
│
├── template.sh
├── setup.py
├── .env
└── README.md
```
## 🏛️ Architecture Diagram
```markdown
## 🏛️ System Architecture
```
```text
                ┌────────────────────┐
                │   User (Browser)   │
                │  Streamlit Frontend│
                └─────────┬──────────┘
                          │
                          │ HTTP POST (Question)
                          ▼
                ┌──────────────────────┐
                │   FastAPI Backend    │
                │  (Async + Middleware)│
                └─────────┬────────────┘
                          │
            ┌─────────────▼─────────────┐
            │  RAG Pipeline (LangChain) │
            │  • Retriever              │
            │  • Prompt                 │
            │  • LLM                    │
            └──────┬──────────────────┬─┘
                   │                  │
          ┌────────▼───────┐   ┌──────▼────────┐
          │ Pinecone Vector│   │  LLM Engine   │
          │   Database     │   │ (Ollama / HF) │
          └────────────────┘   └───────────────┘
```



---

## 🔄 How the System Works (RAG Flow)

1. 📥 User enters a medical question
2. 🔍 Relevant documents retrieved from Pinecone
3. 🧠 Retrieved context passed to LLM
4. ✍️ Answer generated using context
5. 📤 Clean response returned to UI

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/AI_Medical_ChatBot.git
cd AI_Medical_ChatBot
```

### 2️⃣ Create Virtual Environment
```bash
conda create -n medibot python=3.10
conda activate medibot
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
## 🔐 Environment Variables (.env)
```env
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_environment
PINECONE_INDEX_NAME=medical-chatbot
BACKEND_URL=http://127.0.0.1:8000/medicalchatbot
```
## 📦 Create Pinecone Index
```
cd backend/src
python store_index.py
```
This :

- Loads PDFs

- Splits documents

- Generates embeddings

- Stores vectors in Pinecone

### ▶️ Run the Backend
```bash
cd backend/src
uvicorn main:app --reload
```
API will be available at:
```cpp
http://127.0.0.1:8000
```
### 🖥️ Run the Frontend
```bash
cd frontend
streamlit run app.py
```
## 🔌 API Endpoints
| Method | Endpoint          | Description          |
| ------ | ----------------- | -------------------- |
| GET    | `/`               | Root message         |
| GET    | `/health`         | Health check         |
| POST   | `/medicalchatbot` | Ask medical question |

## 🧪 Sample Request
```json
{
  "question": "What is acne?"
}
```
Sample Response
```json
{
  "answer": "Acne is a common skin condition caused by clogged pores..."
}
```

## 🛡️ Middleware Used

- Request logging

- Response time tracking

- Request ID generation

- Centralized error handling

## ⚠️ Disclaimer

This chatbot is for educational purposes only.

It is not a substitute for professional medical advice, diagnosis, or treatment.

Always consult a qualified healthcare provider.

## 🌟 Future Enhancements

- 🔐 Authentication & rate limiting

- 📊 Admin analytics dashboard

- 🧬 More medical datasets

- 🌍 Multi-language support

- 🧪 Unit & integration tests

## 👨‍💻 Author

Shiva Kumar

📧 Email: kshivayadav7@gmail.com

🔗 LinkedIn: (https://www.linkedin.com/in/shiva-kumar-5586432b0/)