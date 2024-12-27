from app.utils.util import read_config
from app.vectordb.data_processor import process_and_add_to_collector
import logging

def insert_data(user_input_data):
    """
    This function handles the logic of pushing the data to vectorDB
    """
    try:
        process_and_add_to_collector(corpus=user_input_data.get('text'), 
                                     clear_collector_before_adding=True)
    except Exception as err:
        logging.info(f'Error in adding user-data to vectordb. Error {err}')
        raise err