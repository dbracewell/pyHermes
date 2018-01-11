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

    def read(self, source: [str, Resource], preprocessors=None, params=None):
        r = resource(source)
        params = to_lower(params)
        language = Language.of(params["language"]) if "language" in params else ENGLISH
        pattern = params["pattern"] if "pattern" in params else '*.*'
        recursive = params["recursive"] if "recursive" in params else True
        generator = filter(lambda f: not f.is_dir(), r.children(recursive=recursive, pattern=pattern)) if r.is_dir() \
            else [r]
        for file in generator:
            yield self._convert(content=file.read(params), language=language, preprocessors=preprocessors,
                                params=params)

    def size(self, source: [str, Resource], params=None) -> int:
        r = resource(source)
        params = to_lower(params)
        pattern = params["pattern"] if "pattern" in params else '*.*'
        recursive = params["recursive"] if "recursive" in params else True
        size = 0
        if r.is_dir():
            for d in r.children(recursive=recursive, pattern=pattern):
                if not d.is_dir():
                    size += self._size(r, params)
        else:
            size += self._size(r, params)

        return size

    def _size(self, resource, params):
        return 1

    def _convert(self, content: str, language, preprocessors, params) -> Document:
        raise NotImplementedError


class OnePerLine(CorpusFormat):
    def __init__(self, wrapped: CorpusFormat):
        self._sub = wrapped

    def _size(self, resource, params):
        size = 0
        with resource.reader(params) as rdr:
            for line in rdr:
                if len(line.rstrip()) > 0:
                    size += 1
        return size

    def read(self, source: [str, Resource], preprocessors=None, params=None):
        r = resource(source)
        params = to_lower(params)
        pattern = params["pattern"] if "pattern" in params else '*.*'
        recursive = params["recursive"] if "recursive" in params else True
        generator = filter(lambda f: not f.is_dir(), r.children(recursive=recursive, pattern=pattern)) if r.is_dir() \
            else [r]
        for file in generator:
            yield self.__process_file(f=file, preprocessors=preprocessors, params=params)

    def __process_file(self, f, preprocessors, params):
        with f.reader(params) as rdr:
            for line in rdr:
                if len(line.strip()) > 0:
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
