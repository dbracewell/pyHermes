from .formats import CorpusFormat
from hermes.core import Document
from hermes.resource import Resource
import hermes.ml.featurizer as ml
import typing
import logging

_logger = logging.getLogger("corpus")


class Corpus:
    def __init__(self, fmt: [str, CorpusFormat], source: [str, Resource] = None, preprocessors=None,
                 params=None) -> None:
        self._fmt = fmt if isinstance(fmt, CorpusFormat) else CorpusFormat.of(fmt)
        self._source = source
        self._params = params
        self._preprocessors = preprocessors

    @staticmethod
    def disk(fmt: [str, CorpusFormat], source: [str, Resource] = None, preprocessors=None, params=None) -> 'Corpus':
        return FileCorpus(fmt=fmt, source=source, preprocessors=preprocessors, params=params)

    def __iter__(self):
        for doc in self.generator():
            yield doc

    def __len__(self):
        return 0

    def generator(self) -> typing.Generator[Document, None, None]:
        raise NotImplementedError

    def cache(self) -> 'Corpus':
        return self

    def to_x_y(self, featurizer: ml.Extractor, label_attr=None):
        x = []
        y = []
        cnt = 0
        for doc in self:
            x.append(featurizer.extract(doc))
            if label_attr:
                y.append(doc[label_attr])
            cnt += 1
            if cnt % 500 == 0:
                _logger.info('Processed %s documents', cnt)
        return x, y


class MemoryCorpus(Corpus):
    def __init__(self, fmt: [str, CorpusFormat]):
        super().__init__(fmt)
        self.docs = []

    def generator(self) -> typing.Generator[Document, None, None]:
        for doc in self.docs:
            yield doc

    def __len__(self):
        return len(self.docs)


class FileCorpus(Corpus):
    def __init__(self, fmt: [str, CorpusFormat], source: [str, Resource] = None, preprocessors=None,
                 params=None):
        super().__init__(fmt, source=source, preprocessors=preprocessors, params=params)

    def generator(self) -> typing.Generator[Document, None, None]:
        return self._fmt.read(source=self._source, preprocessors=self._preprocessors, params=self._params)

    def cache(self) -> 'Corpus':
        mem = MemoryCorpus(fmt=self._fmt)
        for doc in self:
            mem.docs.append(doc)
        return mem

    def __len__(self):
        return self._fmt.size(self._source, self._params)
