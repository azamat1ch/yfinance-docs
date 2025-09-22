"""Utility script to ingest markdown docs into a Chroma collection."""
from __future__ import annotations

import argparse
import glob
import hashlib
import os
from pathlib import Path
from typing import Any, Iterable, Iterator, List, Sequence, Tuple

from dotenv import load_dotenv
from google import genai
import chromadb

DEFAULT_DOCS_GLOB = "docs/**/*.md"
DEFAULT_CHROMA_PATH = "chroma_db"
DEFAULT_COLLECTION = "docs"
DEFAULT_EMBED_MODEL = "gemini-embedding-001"


def chunk_text(text: str, max_words: int, overlap_words: int) -> Iterator[str]:
    """Yield word-level sliding window chunks.

    Parameters
    ----------
    text:
        Raw markdown/text content.
    max_words:
        Target number of words per chunk.
    overlap_words:
        Word overlap between consecutive chunks to preserve context.
    """
    tokens = text.split()
    if not tokens:
        return

    window = max(max_words, 1)
    stride = max(window - max(overlap_words, 0), 1)

    for start in range(0, len(tokens), stride):
        chunk_tokens = tokens[start : start + window]
        chunk = " ".join(chunk_tokens).strip()
        if chunk:
            yield chunk


def make_chunk_id(source: str, index: int, content: str) -> str:
    digest = hashlib.sha1(f"{source}:{index}:{content}".encode("utf-8")).hexdigest()
    return f"{source}:{index}:{digest[:12]}"


def embed_text(client: genai.Client, model: str, text: str) -> Sequence[float]:
    response = client.models.embed_content(model=model, contents=text)
    return response.embeddings[0].values


def flush_batch(
    collection: Any,
    batch: List[Tuple[str, str, dict, Sequence[float]]],
) -> None:
    if not batch:
        return

    ids, documents, metadatas, embeddings = zip(*batch)
    collection.upsert(ids=list(ids), documents=list(documents), metadatas=list(metadatas), embeddings=list(embeddings))
    batch.clear()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest markdown docs into Chroma.")
    parser.add_argument("--docs-glob", default=DEFAULT_DOCS_GLOB, help="Glob pattern for markdown docs")
    parser.add_argument("--chroma-path", default=DEFAULT_CHROMA_PATH, help="Path to persistent Chroma storage")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION, help="Chroma collection name")
    parser.add_argument("--embed-model", default=DEFAULT_EMBED_MODEL, help="Gemini embedding model name")
    parser.add_argument("--max-words", type=int, default=320, help="Max words per chunk")
    parser.add_argument("--overlap-words", type=int, default=60, help="Word overlap between chunks")
    parser.add_argument("--batch-size", type=int, default=32, help="Number of chunks to upsert in a batch")
    return parser.parse_args()


def resolve_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY", "AIzaSyD8TMh3sNO0eur1V95UBDHmga_Y4yEh1pY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Export it or add it to a .env file.")
    return api_key


def collect_files(pattern: str) -> Iterable[Path]:
    for path in glob.glob(pattern, recursive=True):
        file_path = Path(path)
        if file_path.is_file():
            yield file_path


def main() -> None:
    args = parse_args()

    api_key = resolve_api_key()
    client = genai.Client(api_key=api_key)

    chroma_client = chromadb.PersistentClient(path=args.chroma_path)
    collection = chroma_client.get_or_create_collection(args.collection)

    files = sorted(collect_files(args.docs_glob))
    if not files:
        print(f"No files matched pattern '{args.docs_glob}'. Nothing to ingest.")
        return

    total_chunks = 0
    batch: List[Tuple[str, str, dict, Sequence[float]]] = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for index, chunk in enumerate(chunk_text(text, args.max_words, args.overlap_words)):
            chunk_id = make_chunk_id(str(path), index, chunk)
            embedding = embed_text(client, args.embed_model, chunk)
            metadata = {"source": str(path), "chunk_index": index}
            batch.append((chunk_id, chunk, metadata, embedding))
            total_chunks += 1

            if len(batch) >= args.batch_size:
                flush_batch(collection, batch)

    flush_batch(collection, batch)

    print(
        f"Ingested {total_chunks} chunk{'s' if total_chunks != 1 else ''} "
        f"into collection '{args.collection}' at '{args.chroma_path}'."
    )


if __name__ == "__main__":
    main()
