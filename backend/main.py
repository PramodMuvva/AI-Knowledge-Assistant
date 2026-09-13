import chromadb
from google import genai
from dotenv import load_dotenv
import os
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.ingest import ingest_document
from pydantic import BaseModel


load_dotenv()


# -----------------------------
# FastAPI
# -----------------------------

app = FastAPI(
    title="AI Knowledge Assistant API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_DIR = "data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------
# ChromaDB
# -----------------------------

chroma_client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = chroma_client.get_collection(
    name="knowledge_base"
)


# -----------------------------
# Gemini
# -----------------------------

gemini_client = genai.Client()


# -----------------------------
# Request model
# -----------------------------

class QuestionRequest(BaseModel):

    question: str


# -----------------------------
# Ask endpoint
# -----------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):

    query = request.question

    # Retrieve relevant chunks
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    # Combine retrieved chunks
    context = "\n\n".join(documents)

    # Build prompt
    prompt = f"""
You are an AI Knowledge Assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. Do not make up information.
3. If the answer cannot be found in the context, say:
"I could not find the answer in the provided document."

Context:
{context}

Question:
{query}
"""

    # Ask Gemini
    response = gemini_client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    # Prepare sources
    sources = []

    for metadata in metadatas:

        sources.append({
            "source": metadata["source"],
            "page": metadata["page"]
        })

    return {
        "answer": response.output_text,
        "sources": sources
    }
@app.post("/upload")
def upload_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = ingest_document(
        file_path,
        file.filename
    )

    return {
        "message": "Document uploaded and indexed successfully.",
        "filename": file.filename,
        "pages": result["pages"],
        "chunks": result["chunks"]
    }