from ..resource import Resource, resource
from ..core import Document
from ..util import to_lower
from ..language import Language, ENGLISH
import typing

_mapping = {}


class CorpusFormat:
    @staticmethod
    def of(fmt: str) -> 'CorpusFormat':
        fmt = fmt.lower()
        if fmt.endswith("_opl"):
            fmt = fmt[:-4]
            return OnePerLine(_mapping[fmt])
        return _mapping[fmt]

    def read(self, source: [str, Resource], preprocessors=None, params=None) -> typing.Generator[Document, None, None]:
        r = resource(source)
        params = to_lower(params)
        language = Language.of(params["language"]) if "language" in params else ENGLISH
        pattern = params["pattern"] if "pattern" in params else '*.*'
        recursive = params["recursive"] if "recursive" in params else True
        if r.is_dir():
            for d in r.children(recursive=recursive, pattern=pattern):
                if not d.is_dir():
                    yield self._convert(content=d.read(params), language=language, preprocessors=preprocessors,
                                        params=params)
        else:
            yield self._convert(content=r.read(params), language=language, preprocessors=preprocessors, params=params)

    def _convert(self, content: str, language, preprocessors, params) -> Document:
        raise NotImplementedError


class OnePerLine(CorpusFormat):
    def __init__(self, wrapped: CorpusFormat):
        self._sub = wrapped

    def read(self, source: [str, Resource], preprocessors=None, params=None) -> typing.Generator[Document, None, None]:
        r = resource(source)
        params = to_lower(params)
        pattern = params["pattern"] if "pattern" in params else '*.*'
        recursive = params["recursive"] if "recursive" in params else True
        if r.is_dir():
            for d in r.children(recursive=recursive, pattern=pattern):
                if not d.is_dir():
                    for doc in self.__process_file(d, preprocessors=preprocessors, params=params):
                        yield doc
        else:
            for doc in self.__process_file(r, preprocessors=preprocessors, params=params):
                yield doc

    def __process_file(self, f, preprocessors, params) -> typing.Generator[Document, None, None]:
        with f.reader(params) as rdr:
            for line in rdr:
                if len(line.rstrip()) > 0:
                    for d in self._sub.read(resource("string:" + line), preprocessors=preprocessors, params=params):
                        yield d

    def _convert(self, content: str, language, preprocessors, params) -> Document:
        pass


class PlainTextFormat(CorpusFormat):
    def _convert(self, content: str, language, preprocessors, params) -> Document:
        return Document(content=content.rstrip(), language=language, preprocessors=preprocessors)


class JsonFormat(CorpusFormat):
    def _convert(self, content: str, language, preprocessors, params) -> Document:
        return Document.from_json(content)


_mapping["json"] = JsonFormat()
_mapping["txt"] = PlainTextFormat()
