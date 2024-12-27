import logging
from uuid import uuid4

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.vectordb.processor import process_documents

class ChromaDB:
    def __init__(self, collection_name, config):
        self.collection_name = collection_name
        self.config = config
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.get_embedding_model(),
            persist_directory="./app/database"
        )

    def get_embedding_model(self):
        """
        This function helps to gather correct embedding model based on configration on config.json
        """
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        return embeddings

    def add_data_to_collection(self, data_context):
        """
        This function helps to add data to vectorDB. This includes creation a new collection
        or adding data in the same collection
        """
        try:
            documents = process_documents(config=self.config, data_content=data_context.get('text'),
                                          collection_name=self.collection_name)
            uuids = [str(uuid4()) for _ in range(len(documents))]
            self.vector_store.add_documents(documents=documents, ids=uuids)
            logging.info(f'Successfully added data to VectorDB')
            return uuids
        except Exception as err:
            logging.info(f'Error in adding data to VectorDB. Error {err}')
            raise err