import asyncio

from ragbits.document_search import DocumentSearch
from ragbits.document_search.documents.sources import LocalFileSource

from cookbook_rag.embed import get_embedder
from cookbook_rag.partitioner import get_unstructured_partitioner
from src.cookbook_rag.utils import get_root
from src.cookbook_rag.vector_store import get_qdrant_vector_store

documents_path = get_root() / "recipes_docs"
documents = LocalFileSource.list_sources(documents_path, file_pattern="*.pdf")

print("Creating embedder...")
embedder = get_embedder()
print("Creating vector store...")
vector_store = get_qdrant_vector_store()
print("Creating document processor...")
document_processor = get_unstructured_partitioner()

print("Creating document search...")
document_search = DocumentSearch(
    embedder=embedder,
    vector_store=vector_store,
)

if __name__ == "__main__":
    print("Ingesting documents...")
    asyncio.run(
        document_search.ingest(
            documents,
            document_processor=document_processor,
        )
    )