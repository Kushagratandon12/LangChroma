from vectordb.pre_processor import data_clean_up
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

def data_processor(data_processor_config, textual_context):
    """
    This function process the data and move forward with inserting the data to cromadb
    """
    documents = [Document(page_content= textual_context, medata={"source": ''})]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=data_processor_config.get('CHUNK_SIZE', 500),
                                                   chunk_overlap=data_processor_config.get('CHUNK_OVERLAP', 50),
                                                   add_start_index=True)
    text_docs = text_splitter.split_documents(data_clean_up(list_of_documents=documents))