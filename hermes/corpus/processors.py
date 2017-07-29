import typing
from collections import Counter
from .corpus import Corpus


class BaseExtractor:
    def __init__(self, binary=False, to_string=None, annotation_type='token'):
        self._binary = binary
        self._to_string = to_string
        self._annotation_type = annotation_type

    def process(self, corpus: Corpus) -> Counter:
        raise NotImplementedError
