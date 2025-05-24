# multi_agent_tutor/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.tutor_agent import TutorAgent
import uvicorn
import time

app = FastAPI(
    title="Multi-Agent Tutoring Bot",
    description="An AI Tutor that delegates questions to specialist agents (Math, Physics) using Google Gemini.",
    version="0.2.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

tutor_bot = TutorAgent()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"Request: {request.method} {request.url.path} - Completed in {duration:.4f} secs - Status: {response.status_code}")
    return response

@app.get("/", tags=["General"])
async def read_root():
    return {
        "message": "Welcome to the Multi-Agent Tutoring Bot API!",
        "documentation": "/docs",
        "ask_endpoint": "/ask (POST)"
    }

@app.post("/ask", response_model=QueryResponse, tags=["Tutoring"])
async def ask_tutor(request_data: QueryRequest):
    query = request_data.query
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    if len(query) > 1000:
        raise HTTPException(status_code=413, detail="Query is too long (max 1000 characters).")

    try:
        print(f"Received query for /ask: {query}")
        answer = tutor_bot.route_query(query)
        return QueryResponse(answer=answer)
    except Exception as e:
        print(f"An error occurred while processing query '{query}': {e}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")

if __name__ == "__main__":
    print("Starting Uvicorn server for development.")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)