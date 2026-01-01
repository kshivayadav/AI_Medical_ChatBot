from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
import uuid
from rag_pipeline import rag_chain
from schema import ChatRequest,ChatResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title = "Medical Chatbot API",
               version = "1.0.0",
               description="AI-powered Medical Chatbot using RAG architecture")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    response = await call_next(request)

    process_time = round(time.time() - start_time, 3)
    response.headers["X-Request-ID"] = request_id

    logger.info(
        f"[{request_id}] {request.method} {request.url.path} "
        f"- {response.status_code} - {process_time}s"
    )

    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong while processing your request"
        }
    )

@app.get("/",tags=["General"],summary="Root Endpoint")
async def read_root():
    return {"message": "Welcome to the Medical Chatbot API"}


@app.get("/health",tags=["Monitoring"],summary="Health Check")
async def health_check():
    return {"Status": "ok",
            "version": "1.0.0",
            "message":"Medical Chatbot API is Running Successfully"}

@app.post(
        "/medicalchatbot",
        response_model = ChatResponse,
        status_code=status.HTTP_200_OK,
        tags=["Chat"],
        summary="Medical Question Answering"
)
async def medical_chatbot(query:ChatRequest):
    """
    Accepts a medical question and returns an AI-generated answer
    using Retrieval-Augmented Generation (RAG).
    """
    try:
        logger.info(f"Received question: {query.question}")
        response = await run_in_threadpool(
                                    rag_chain.invoke,
                                    {"input": query.question})

        if not response or "answer" not in response:
            logger.error("Invalid response from RAG pipeline")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate answer"
            )
        
        logger.info("Response generated successfully.")

        return ChatResponse(
            answer = response['answer']
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unhandled error occurred")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing the request"
        )


