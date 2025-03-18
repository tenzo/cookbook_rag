from ragbits.core.embeddings.litellm import LiteLLMEmbeddings
from cookbook_rag.config import get_openai_config

def get_embedder():
    config = get_openai_config()
    return LiteLLMEmbeddings(
        model="text-embedding-3-small",
        api_key=config.openai_api_key,
    )