from app.utils.util import read_config
from app.vectordb.cromadb import ChromaDB
import logging

def insert_data(user_input_data):
    """
    This function handles the logic of pushing the data to vectorDB
    """
    try:
        config = read_config(filename="./app/config/config.json")
        chromadb = ChromaDB(config=config.get('MODEL'),collection_name="kushagra")
        uuids = chromadb.add_data_to_collection(data_context=user_input_data)
        return uuids
    except Exception as err:
        logging.info(f'Error in adding user-data to vectordb. Error {err}')
        raise err