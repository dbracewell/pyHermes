from .formats import CorpusFormat
from hermes.core import Document
from hermes.resource import Resource
import typing


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

    def generator(self) -> typing.Generator[Document, None, None]:
        raise NotImplementedError

    def cache(self) -> 'Corpus':
        return self


class MemoryCorpus(Corpus):
    def __init__(self, fmt: [str, CorpusFormat]):
        super().__init__(fmt)
        self.docs = []

    def generator(self) -> typing.Generator[Document, None, None]:
        for doc in self.docs:
            yield doc


class FileCorpus(Corpus):
    def generator(self) -> typing.Generator[Document, None, None]:
        return self._fmt.read(source=self._source, preprocessors=self._preprocessors, params=self._params)

    def cache(self) -> 'Corpus':
        mem = MemoryCorpus(fmt=self._fmt)
        for doc in self:
            mem.docs.append(doc)
        return mem
