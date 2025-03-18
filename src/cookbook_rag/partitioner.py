import asyncio
import json
from io import BytesIO

from ragbits.core.audit import traceable
from ragbits.document_search.documents.document import DocumentMeta, Document
from ragbits.document_search.documents.element import Element
from ragbits.document_search.ingestion.providers.unstructured import UnstructuredPdfProvider
from unstructured.partition.auto import partition
from unstructured.staging.base import elements_from_dicts

from cookbook_rag.config import get_unstructured_config
from cookbook_rag.utils import get_root

partition_kwargs = {
    "strategy": "hi_res",
    "languages": ["eng"],
    "split_pdf_page": True,
    "split_pdf_allow_failed": False,
    "split_pdf_concurrency_level": 15,
}

CACHE_DIR = get_root() / "ingest_cache"

class CachingUnstructuredPdfProvider(UnstructuredPdfProvider):

    def check_cache(self, document: Document) -> bool:
        return CACHE_DIR.joinpath(f"{document.local_path.name}.json").exists()

    def load_cache(self, document: Document) -> list[Element]:
        with open(CACHE_DIR.joinpath(f"{document.local_path.name}.json"), "r") as f:
            return elements_from_dicts(json.load(f))

    def cache_elements(self, elements: list[dict], document: Document) -> None:
        with open(CACHE_DIR.joinpath(f"{document.local_path.name}.json"), "w") as f:
            json.dump(elements, f)

    @traceable
    async def process(self, document_meta: DocumentMeta) -> list[Element]:
        """
        Process the document using the Unstructured API.

        Args:
            document_meta: The document to process.

        Returns:
            The list of elements extracted from the document.

        Raises:
            DocumentTypeNotSupportedError: If the document type is not supported.

        """
        self.validate_document_type(document_meta.document_type)
        document = await document_meta.fetch()

        if self.check_cache(document):
            elements = self.load_cache(document)
            print(f"Loaded {len(elements)} elements for {document.local_path.name} from cache")
        elif self.use_api:
            elements = await asyncio.to_thread(self.partition_blocking, document)
            print(f"Partitioned {len(elements)} elements for {document.local_path.name} via API")
        else:
            elements = partition(
                file=BytesIO(document.local_path.read_bytes()),
                metadata_filename=document.local_path.name,
                **self.partition_kwargs,
            )
            print(f"Partitioned {len(elements)} elements for {document.local_path.name} locally")

        chunked_elements = await self._chunk_and_convert(elements, document_meta, document.local_path)
        print(f"Chunked {len(chunked_elements)} elements for {document.local_path.name}")
        return chunked_elements


    def partition_blocking(self, document: Document) -> list[Element]:
        """
        Partition the document using the Unstructured API. Using the blocking function
        as the async version of partition method does not work correctly in unstructured client.

        Args:
            document: The document to partition.

        Returns:
            The list of elements extracted from the document.
        """
        res = self.client.general.partition(
            request={
                "partition_parameters": {
                    "files": {
                        "content": document.local_path.read_bytes(),
                        "file_name": document.local_path.name,
                    },
                    "coordinates": True,
                    **self.partition_kwargs,
                }
            }
        )
        self.cache_elements(res.elements, document)

        return elements_from_dicts(res.elements)



def get_unstructured_partitioner():
    config = get_unstructured_config()

    return CachingUnstructuredPdfProvider(
        partition_kwargs=partition_kwargs,
        chunking_kwargs={},
        api_key=config.unstructured_api_key,
        api_server=config.unstructured_server_url,
        use_api=True,
        ignore_images=True,
    )