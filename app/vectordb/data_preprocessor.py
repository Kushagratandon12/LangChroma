import nltk
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from num2words import num2words

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Ensure required NLTK resources are downloaded
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

class TextPreprocessorBuilder:
    # Cache for expensive operations
    _lemmatizer_cache = {}
    _pos_remove_cache = {}

    def __init__(self, text: str):
        self.text = text
        self._stop_words = set(stopwords.words('english'))  # Initialize dynamically
        self._lemmatizer = WordNetLemmatizer()  # Initialize dynamically

    def to_lower(self):
        # Match both words and non-word characters
        tokens = re.findall(r'\b\w+\b|\W+', self.text)
        for i, token in enumerate(tokens):
            # Check if token is a word
            if re.match(r'^\w+$', token):
                # Check if token is not an abbreviation or constant
                if not re.match(r'^[A-Z]+$', token) and not re.match(r'^[A-Z_]+$', token):
                    tokens[i] = token.lower()
        self.text = "".join(tokens)
        return self

    def num_to_word(self, min_len: int = 1):
        tokens = re.findall(r'\b\w+\b|\W+', self.text)
        for i, token in enumerate(tokens):
            if token.isdigit() and len(token) >= min_len:
                tokens[i] = num2words(int(token)).replace(",", "")
        self.text = "".join(tokens)
        return self

    def num_to_char_long(self, min_len: int = 1):
        tokens = re.findall(r'\b\w+\b|\W+', self.text)
        for i, token in enumerate(tokens):
            if token.isdigit() and len(token) >= min_len:
                convert_token = lambda token: ''.join((chr(int(digit) + 65) * (i + 1)) for i, digit in enumerate(token[::-1]))[::-1]
                tokens[i] = convert_token(tokens[i])
        self.text = "".join(tokens)
        return self

    def num_to_char(self, min_len: int = 1):
        tokens = re.findall(r'\b\w+\b|\W+', self.text)
        for i, token in enumerate(tokens):
            if token.isdigit() and len(token) >= min_len:
                tokens[i] = ''.join(chr(int(digit) + 65) for digit in token)
        self.text = "".join(tokens)
        return self

    def merge_spaces(self):
        self.text = re.sub(' +', ' ', self.text)
        return self

    def strip(self):
        self.text = self.text.strip()
        return self

    def remove_punctuation(self):
        self.text = self.text.translate(str.maketrans('', '', string.punctuation))
        return self

    def remove_stopwords(self):
        self.text = "".join([word for word in re.findall(r'\b\w+\b|\W+', self.text) if word not in self._stop_words])
        return self

    def remove_specific_pos(self):
        processed_text = TextPreprocessorBuilder._pos_remove_cache.get(self.text)
        if processed_text:
            self.text = processed_text
            return self

        tokens = re.findall(r'\b\w+\b|\W+', self.text)
        excluded_tags = ['RB', 'RBR', 'RBS', 'UH']

        for i, token in enumerate(tokens):
            if re.match(r'^\w+$', token):
                pos = nltk.pos_tag([token])[0][1]
                if pos in excluded_tags:
                    tokens[i] = ''

        new_text = "".join(tokens)
        TextPreprocessorBuilder._pos_remove_cache[self.text] = new_text
        self.text = new_text

        return self

    def lemmatize(self):
        processed_text = TextPreprocessorBuilder._lemmatizer_cache.get(self.text)
        if processed_text:
            self.text = processed_text
            return self

        new_text = "".join([self._lemmatizer.lemmatize(word) for word in re.findall(r'\b\w+\b|\W+', self.text)])
        TextPreprocessorBuilder._lemmatizer_cache[self.text] = new_text
        self.text = new_text

        return self

    def build(self):
        return self.text