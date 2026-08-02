#!/usr/bin/env python3
"""
RAG starter kit for the docs mirror.

Indexes the Markdown pages in this repository into a local ChromaDB
vector store and answers retrieval queries over them. Drop-in for any
*-docs-llm-agents repo.

Setup:
    pip install chromadb

Usage:
    python rag.py build [--dir .]         create/update ./rag_chroma
    python rag.py query "question" [-k 5]  print top-k relevant chunks
    python rag.py info                      print corpus stats

Design notes:
    - Chunks ~900 chars with 120-char overlap, split on blank lines first.
    - Each chunk is upserted keyed by (file, index), so re-running `build`
      is idempotent and cheap.
    - Uses ChromaDB's default embedding (ONNX all-MiniLM-L6-v2, ~80 MB
      downloaded on first run). Override with --embedding if needed.
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "rag_chroma"
CHUNK_SIZE = 900
OVERLAP = 120
FRONTMATTER = re.compile(r"^---\n.*?\n---\n", re.S)
BIG_META = re.compile(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>")


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    text = FRONTMATTER.sub("", text)
    text = BIG_META.sub("", text)
    step = max(1, size - overlap)
    chunks = []
    for i in range(0, len(text), step):
        chunk = text[i : i + size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def iter_md_files(doc_dir: Path):
    if doc_dir.is_file():
        yield doc_dir
        return
    for f in sorted(doc_dir.rglob("*.md")):
        yield f


def cmd_build(args) -> None:
    import chromadb

    doc_dir = ROOT / args.dir
    if not doc_dir.exists():
        sys.exit(f"error: {doc_dir} not found")
    db = ROOT / args.db
    client = chromadb.PersistentClient(path=str(db))
    col = client.get_or_create_collection(
        "docs", metadata={"hnsw:space": "cosine"}
    )
    total = 0
    for f in iter_md_files(doc_dir):
        text = f.read_text(encoding="utf-8", errors="replace")
        for i, chunk in enumerate(chunk_text(text)):
            cid = hashlib.md5(f"{f.as_posix()}#{i}".encode()).hexdigest()
            col.upsert(
                ids=[cid],
                documents=[chunk],
                metadatas=[{"source": str(f.relative_to(ROOT)), "chunk": i}],
            )
            total += 1
    print(f"indexed {total} chunks from {doc_dir} into {db}")


def cmd_query(args) -> None:
    import chromadb

    db = ROOT / args.db
    if not (db / "chroma.sqlite3").exists():
        sys.exit(f"error: no index at {db}. Run `python rag.py build` first.")
    client = chromadb.PersistentClient(path=str(db))
    col = client.get_collection("docs")
    res = col.query(query_texts=[args.query], n_results=args.k)
    if not res["documents"] or not res["documents"][0]:
        print("no results")
        return
    for meta, doc, dist in zip(
        res["metadatas"][0], res["documents"][0], res["distances"][0]
    ):
        src = meta["source"]
        print(f"\n## {src} (distance {dist:.4f})\n")
        print(doc[: args.context])


def cmd_info(args) -> None:
    import chromadb

    db = ROOT / args.db
    if not (db / "chroma.sqlite3").exists():
        sys.exit(f"error: no index at {db}. Run `python rag.py build` first.")
    col = chromadb.PersistentClient(path=str(db)).get_collection("docs")
    print(f"collection: {col.count()} chunks")
    metas = col.get(include=["metadatas"])["metadatas"]
    sources = sorted({m["source"] for m in metas if m})
    print(f"sources: {len(sources)}")
    for s in sources:
        print(f"  - {s}")


def main() -> None:
    ap = argparse.ArgumentParser(description="RAG starter kit for the docs mirror")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="ChromaDB path")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="index Markdown pages into ChromaDB")
    b.add_argument("--dir", default=".", help="directory of Markdown pages")

    q = sub.add_parser("query", help="retrieve top-k chunks for a question")
    q.add_argument("query")
    q.add_argument("-k", type=int, default=5)
    q.add_argument("--context", type=int, default=3000, help="chars per result")

    sub.add_parser("info", help="show index stats")

    args = ap.parse_args()
    if args.cmd == "build":
        cmd_build(args)
    elif args.cmd == "query":
        cmd_query(args)
    else:
        cmd_info(args)


if __name__ == "__main__":
    main()
