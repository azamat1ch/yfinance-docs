"""FastAPI application powering the docs chat experience."""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, List, Sequence

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
import chromadb

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "docs")
EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")
GENERATE_MODEL = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash")
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))
MAX_CONTEXT_SECTIONS = int(os.getenv("RAG_MAX_CONTEXT", "5"))

ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("RAG_ALLOWED_ORIGINS", "*").split(",") if origin.strip()]
ALLOWED_HEADERS = ["*"]
ALLOWED_METHODS = ["GET", "POST", "OPTIONS"]


class ChatIn(BaseModel):
    query: str = Field(..., description="User query to answer using the docs")


class ChatOut(BaseModel):
    answer: str
    sources: List[str]


@lru_cache(maxsize=1)
def get_genai_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Set it in the environment or a .env file.")
    return genai.Client(api_key=api_key)


@lru_cache(maxsize=1)
def get_chroma_collection() -> Any:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(COLLECTION_NAME)


def embed_query(text: str) -> Sequence[float]:
    client = get_genai_client()
    response = client.models.embed_content(model=EMBED_MODEL, contents=text)
    return response.embeddings[0].values


def format_context(documents: Sequence[str], metadatas: Sequence[Dict[str, Any]]) -> str:
    sections: List[str] = []
    for idx, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
        source = meta.get("source", "unknown source")
        chunk_index = meta.get("chunk_index")
        label = f"[{idx}] {source}"
        if chunk_index is not None:
            label = f"{label} (chunk {chunk_index})"
        sections.append(f"{label}\n{doc}")
    return "\n\n".join(sections)


def collect_sources(metadatas: Sequence[Dict[str, Any]]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for meta in metadatas:
        source = meta.get("source")
        if not source or source in seen:
            continue
        seen.add(source)
        ordered.append(source)
    return ordered


def build_prompt(context: str, question: str) -> str:
    return (
        "You are a helpful assistant for the Yahoo Finance Docs website. "
        "Answer the question using ONLY the provided context. If the context "
        "does not contain the answer, say you do not know. Include numbered "
        "citations like [1] that refer to the matching context section.\n\n"
        f"Context:\n{context}\n\nQuestion:\n{question}\n\n"
        "Write a concise answer first, then list the citations inline."
    )


def generate_answer(prompt: str) -> str:
    client = get_genai_client()
    response = client.models.generate_content(model=GENERATE_MODEL, contents=prompt)
    text = getattr(response, "text", None)
    if text:
        return text.strip()
    if hasattr(response, "candidates"):
        for candidate in response.candidates or []:
            parts = getattr(candidate, "content", None)
            if not parts:
                continue
            for part in getattr(parts, "parts", []):
                text_part = getattr(part, "text", None)
                if text_part:
                    return text_part.strip()
    return "I couldn't generate a response."


app = FastAPI(title="Docs RAG API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatOut)
async def chat(payload: ChatIn) -> ChatOut:
    question = payload.query.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Query must not be empty.")

    try:
        query_embedding = embed_query(question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to embed query: {exc}") from exc

    collection = get_chroma_collection()
    try:
        results = collection.query(query_embeddings=[query_embedding], n_results=RAG_TOP_K)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Vector store query failed: {exc}") from exc

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return ChatOut(
            answer="I couldn't find anything relevant in the indexed documentation.",
            sources=[],
        )

    context = format_context(documents[:MAX_CONTEXT_SECTIONS], metadatas[:MAX_CONTEXT_SECTIONS])
    prompt = build_prompt(context, question)

    try:
        answer = generate_answer(prompt)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {exc}") from exc

    sources = collect_sources(metadatas)
    return ChatOut(answer=answer, sources=sources)


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Docs RAG API"}
