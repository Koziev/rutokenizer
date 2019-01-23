from __future__ import absolute_import
from .tokenizer import Tokenizer
from .corpustokenizer import CorpusTokenizer
from .segmenter import Segmenter
from .tokenizer import tokenizer_tests

def run_tests():
    tokenizer_tests()
