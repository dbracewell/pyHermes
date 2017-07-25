from ..resource import Resource, resource
from ..core import Document
from ..util import to_lower
from ..language import Language, ENGLISH


class CorpusFormat:
    def read(self, source: [str, Resource], preprocessors=None, params=None):
        raise NotImplementedError


class OnePerLine(CorpusFormat):
    def read(self, source: [str, Resource], preprocessors=None, params=None):
        r = resource(source)
        with r.reader(params) as rdr:
            for line in rdr:
                for d in self._sub.read(resource("string:" + line), preprocessors, params):
                    yield d

    def __init__(self, wrapped: CorpusFormat):
        self._sub = wrapped


class PlainTextFormat(CorpusFormat):
    def read(self, source: [str, Resource], preprocessors=None, params=None):
        r = resource(source)
        params = to_lower(params)
        language = Language.of(params["language"]) if "langauge" in params else ENGLISH
        yield Document(content=r.read(params), language=language, preprocessors=preprocessors)


class JsonFormat(CorpusFormat):
    def read(self, source: [str, Resource], preprocessors=None, params=None):
        r = resource(source)
        yield Document.from_json(r.read())
