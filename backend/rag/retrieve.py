from typing import List, Dict, Any
from .vectordb import get_vectordb

def retrieve_with_citations(query: str, k: int = 6) -> Dict[str, Any]:
    vectordb = get_vectordb()
    docs = vectordb.similarity_search(query, k=k)

    citations = []
    context_blocks = []

    for d in docs:
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", "?")
        snippet = d.page_content[:350].replace("\n", " ").strip()

        citations.append({"source": src, "page": page, "snippet": snippet})
        context_blocks.append(f"[{src} - page {page}]\n{d.page_content}")

    context = "\n\n---\n\n".join(context_blocks).strip()
    return {"context": context, "citations": citations}
