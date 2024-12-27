import threading
import chromadb
import random
import logging
from chromadb.config import Settings
from chromadb.utils import embedding_functions

class ChromaCollector:
    def __init__(self):
        super().__init__()
        # Initialize the ChromaDB client
        self.chroma_client = chromadb.PersistentClient(
            path='./app/database',
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )
        self.embedder = embedding_functions.HuggingFaceEmbeddingFunction(model_name="sentence-transformers/all-mpnet-base-v2")
        # Generate a random name for the collection
        self.name = ''.join(random.choice('vec') for _ in range(5))
        self.collection = self.chroma_client.create_collection(
            name=self.name,
            embedding_function=self.embedder
        )

        # Initialize storage variables
        self.ids = []
        self.id_to_info = {}
        self.embeddings_cache = {}
        self.lock = threading.Lock()  # Ensure thread safety

    def add(self, texts: list[str], texts_with_context: list[str], starting_indices: list[int], metadatas: list[dict] = None):
        with self.lock:
            # Validate input lengths
            assert metadatas is None or len(metadatas) == len(texts), "metadatas must be None or have the same length as texts"
            if len(texts) == 0:
                return

            # Generate new IDs for the documents
            new_ids = self._get_new_ids(len(texts))

            # Split texts into existing and non-existing based on cache
            (existing_texts, existing_embeddings, existing_ids, existing_metas), \
            (non_existing_texts, non_existing_ids, non_existing_metas) = self._split_texts_by_cache_hit(
                texts, new_ids, metadatas
            )

            # Add existing embeddings (from cache)
            if existing_texts:
                logging.info(f'Adding {len(existing_embeddings)} cached embeddings.')
                args = {'embeddings': existing_embeddings, 'documents': existing_texts, 'ids': existing_ids}
                if existing_metas:
                    args['metadatas'] = existing_metas
                self.collection.add(**args)

            # Add new embeddings (compute them first)
            if non_existing_texts:
                non_existing_embeddings = self.embedder(non_existing_texts)
                for text, embedding in zip(non_existing_texts, non_existing_embeddings):
                    self.embeddings_cache[text] = embedding

                logging.info(f'Adding {len(non_existing_embeddings)} new embeddings.')
                args = {'embeddings': non_existing_embeddings, 'documents': non_existing_texts, 'ids': non_existing_ids}
                if non_existing_metas:
                    args['metadatas'] = non_existing_metas
                self.collection.add(**args)

            # Update ID-to-context mapping
            new_info = {
                id_: {'text_with_context': context, 'start_index': start_index}
                for id_, context, start_index in zip(new_ids, texts_with_context, starting_indices)
            }
            self.id_to_info.update(new_info)
            self.ids.extend(new_ids)

    def _split_texts_by_cache_hit(self, texts: list[str], new_ids: list[str], metadatas: list[dict]):
        # Split texts into "existing in cache" and "non-existing in cache"
        existing_texts, non_existing_texts = [], []
        existing_embeddings = []
        existing_ids, non_existing_ids = [], []
        existing_metas, non_existing_metas = [], []

        for i, text in enumerate(texts):
            id_ = new_ids[i]
            metadata = metadatas[i] if metadatas is not None else None
            embedding = self.embeddings_cache.get(text)
            if embedding is not None:  # Cache hit
                existing_texts.append(text)
                existing_embeddings.append(embedding)
                existing_ids.append(id_)
                if metadata:
                    existing_metas.append(metadata)
            else:  # Cache miss
                non_existing_texts.append(text)
                non_existing_ids.append(id_)
                if metadata:
                    non_existing_metas.append(metadata)

        return (existing_texts, existing_embeddings, existing_ids, existing_metas), \
               (non_existing_texts, non_existing_ids, non_existing_metas)

    def _get_new_ids(self, num_new_ids: int):
        # Generate unique IDs for new entries
        max_existing_id = max(int(id_) for id_ in self.ids) if self.ids else -1
        return [str(i + max_existing_id + 1) for i in range(num_new_ids)]

    def persist_directory(self):
        logging.info(f'Default Persist Directory: {self.chroma_client.get_settings()}')