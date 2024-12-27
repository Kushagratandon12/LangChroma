import json
import sys
import logging

def read_config(filename):
    """
    This function helps to read config of your code
    """
    try:
        with open(filename, "r") as fp:
            config_json = json.load(fp)
            logging.info(f'Config.json loaded successfully')
        return config_json

    except Exception as err:
        logging.error(f'Error in loading config. Error: {err}')
        sys.exit(1)