from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.vectordb.pre_processor import clean_documents
from langchain_core.documents import Document

def process_documents(config, data_content, collection_name):
    """
    This function process the documents , split documents based on configration on config.
    """
    docs = [Document(page_content=data_content, metadata={'source': collection_name})]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.get('chunk_size',500),
                                                   chunk_overlap=config.get('chunk_overlap',50),
                                                   add_start_index=True)
    text_docs = text_splitter.split_documents(clean_documents(list_of_documents=docs))
    return text_docs

