from qdrant_client import AsyncQdrantClient
from ragbits.core.vector_stores.qdrant import QdrantVectorStore

from src.cookbook_rag.config import get_qdrant_config


def get_qdrant_vector_store():
    config = get_qdrant_config()
    return QdrantVectorStore(
        client=AsyncQdrantClient(
            url=config.qdrant_url,
            port=config.qdrant_port,
        ),
        index_name=config.qdrant_index_name,
    )