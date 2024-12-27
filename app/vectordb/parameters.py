from pathlib import Path

import json
import logging


NUM_TO_WORD_METHOD = 'Number to Word'
NUM_TO_CHAR_METHOD = 'Number to Char'
NUM_TO_CHAR_LONG_METHOD = 'Number to Multi-Char'


DIST_MIN_STRATEGY = 'Min of Two'
DIST_HARMONIC_STRATEGY = 'Harmonic Mean'
DIST_GEOMETRIC_STRATEGY = 'Geometric Mean'
DIST_ARITHMETIC_STRATEGY = 'Arithmetic Mean'


PREPEND_TO_LAST = 'Prepend to Last Message'
APPEND_TO_LAST = 'Append to Last Message'
HIJACK_LAST_IN_CONTEXT = 'Hijack Last Message in Context ⚠️ WIP ⚠️ (Works Partially)'


SORT_DISTANCE = 'distance'
SORT_ID = 'id'


class Parameters:
    _instance = None

    variable_mapping = {
        'NUM_TO_WORD_METHOD': NUM_TO_WORD_METHOD,
        'NUM_TO_CHAR_METHOD': NUM_TO_CHAR_METHOD,
        'NUM_TO_CHAR_LONG_METHOD': NUM_TO_CHAR_LONG_METHOD,
        'DIST_MIN_STRATEGY': DIST_MIN_STRATEGY,
        'DIST_HARMONIC_STRATEGY': DIST_HARMONIC_STRATEGY,
        'DIST_GEOMETRIC_STRATEGY': DIST_GEOMETRIC_STRATEGY,
        'DIST_ARITHMETIC_STRATEGY': DIST_ARITHMETIC_STRATEGY,
        'PREPEND_TO_LAST': PREPEND_TO_LAST,
        'APPEND_TO_LAST': APPEND_TO_LAST,
        'HIJACK_LAST_IN_CONTEXT': HIJACK_LAST_IN_CONTEXT,
    }

    @staticmethod
    def getInstance():
        if Parameters._instance is None:
            Parameters()
        return Parameters._instance

    def __init__(self):
        if Parameters._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Parameters._instance = self
            self.hyperparameters = self._load_from_json(Path("./app/config/config.json"))

    def _load_from_json(self, file_path):
        logging.debug('Loading hyperparameters...')

        with open(file_path, 'r') as file:
            data = json.load(file)

        # Replace variable names in the dict and create Categorical objects
        for key in data:
            if "default" in data[key] and data[key]["default"] in self.variable_mapping:
                data[key]["default"] = self.variable_mapping[data[key]["default"]]
            if "categories" in data[key]:
                data[key]["categories"] = [self.variable_mapping.get(cat, cat) for cat in data[key]["categories"]]

        return data


def should_to_lower() -> bool:
    return bool(Parameters.getInstance().hyperparameters['to_lower']['default'])


def get_num_conversion_strategy() -> str:
    return Parameters.getInstance().hyperparameters['num_conversion']['default']


def should_merge_spaces() -> bool:
    return bool(Parameters.getInstance().hyperparameters['merge_spaces']['default'])


def should_strip() -> bool:
    return bool(Parameters.getInstance().hyperparameters['strip']['default'])


def should_remove_punctuation() -> bool:
    return bool(Parameters.getInstance().hyperparameters['remove_punctuation']['default'])


def should_remove_stopwords() -> bool:
    return bool(Parameters.getInstance().hyperparameters['remove_stopwords']['default'])


def should_remove_specific_pos() -> bool:
    return bool(Parameters.getInstance().hyperparameters['remove_specific_pos']['default'])


def should_lemmatize() -> bool:
    return bool(Parameters.getInstance().hyperparameters['lemmatize']['default'])


def get_context_len() -> str:
    context_len = str(Parameters.getInstance().hyperparameters['context_len_left']['default']) + ',' + str(Parameters.getInstance().hyperparameters['context_len_right']['default'])
    return context_len


def get_min_num_length() -> int:
    return int(Parameters.getInstance().hyperparameters['min_num_length']['default'])


def get_chunk_separator() -> str:
    return Parameters.getInstance().hyperparameters['chunk_separator']['default']


def get_chunk_regex() -> str:
    return Parameters.getInstance().hyperparameters['chunk_regex']['default']

def get_delta_start() -> int:
    return int(Parameters.getInstance().hyperparameters['delta_start']['default'])