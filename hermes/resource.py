import io
from pathlib import Path
from typing import List, Dict, Any, Union
import urllib.request as request
import urllib.parse as urlparse
import zlib
from os.path import splitext
import pickle
import fnmatch

"""
   Copyright 2017 David B. Bracewell

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


class Resource(object):
    """
    Abstraction of a resource (e.g. file, string, url) that can be read from or written to.
    """

    def reader(self, params=None):
        """
        Opens the resource in read mode
        :param params: parameters to be used in the open (specific to each implementation)
        :return: a stream that can be read from
        """
        raise NotImplementedError

    def writer(self, params=None):
        """
        Opens the resource in write mode
        :param params: parameters to be used in the open (specific to each implementation)
        :return: a stream that can be written to
        """
        raise NotImplementedError

    def read(self, params=None) -> str:
        """
        Reads the resource into a string
        :param params: parameters to be used in the open (specific to each implementation)
        :return: the string contents of the resource
        """
        encoding = params["encoding"] if "encoding" in params else "utf-8"
        compression = params["compress"] if "compress" in params else False
        if compression:
            params["mode"] = "rb"
        with self.reader(params) as reader:
            if compression:
                return zlib.decompress(reader.read()).decode(encoding)
            return reader.read()

    def readlines(self, params=None) -> List[str]:
        """
        Reads the resource line by line into a list of strings
        :param params: parameters to be used in the open (specific to each implementation)
        :return: the string contents of the resource
        """
        return self.read(params).splitlines()

    def write(self, content: str, params=None) -> None:
        """
        Writes the given content to the resource
        :param content: The content to write
        :param params: parameters to be used in the open (specific to each implementation)
        :return: None
        """
        encoding = params["encoding"] if "encoding" in params else "utf-8"
        compression = params["compress"] if "compress" in params else False
        if compression:
            params["mode"] = "wb"
        with self.writer(params) as writer:
            if compression:
                writer.write(zlib.compress(content.encode(encoding)))
            else:
                writer.write(content)

    def descriptor(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.descriptor()

    def __repr__(self) -> str:
        return self.descriptor()

    def path(self) -> str:
        """
        :return: The path of the resource
        """
        return ""

    def ext(self) -> str:
        """
        :return: the extension of the file
        """
        return ""

    def basename(self) -> str:
        """
        :return: the basename of the file
        """
        return ""

    def children(self, recursive: bool = False, pattern='*.*') -> List['Resource']:
        """
        :return: child resources
        """
        return []

    def child(self, subpath: str) -> 'Resource':
        """
        Gets a resource relative to this one
        :param subpath: The subpath
        :return: A resource relative to this one
        """
        return self

    def parent(self) -> 'Resource':
        """
        Gets the parent (resource) (i.e. one level up)
        :return:  The parent resource
        """
        return self

    def is_dir(self) -> bool:
        """
        :return: True if this resource represents a directory
        """
        return False

    def exists(self) -> bool:
        """
        :return: True if the resource exists
        """
        return True

    def mkdirs(self) -> None:
        """
        Makes all directories down to and including this one
        :return: None
        """
        pass

    def write_object(self, object):
        with self.writer({"mode": "wb"}) as w:
            pickle.dump(object, w)

    def read_object(self):
        with self.reader({"mode": "rb"}) as r:
            return pickle.load(r)

    def _mkparams(self, params: Dict[str, Any]):
        if params is None:
            return {}
        return dict([(k.lower(), v) for k, v in params.items()])


class FileResource(Resource):
    """
    Wraps local file based resource
    """

    def __init__(self, location):
        if isinstance(location, Path):
            self._location = location
        else:
            self._location = Path(location)

    def reader(self, params=None):
        params = self._mkparams(params)
        encoding = params["encoding"] if "encoding" in params else "utf-8"
        mode = params["mode"] if "mode" in params else "r"
        if "b" in mode:
            return self._location.open(mode)
        return self._location.open(encoding=encoding)

    def children(self, recursive: bool = False, pattern: str = '*.*') -> List['Resource']:
        for f in self._location.iterdir():
            try:
                r = FileResource(f)
                if recursive and r.is_dir():
                    for cc in r.children(recursive):
                        yield cc
                elif fnmatch.fnmatch(r.path(), pattern):
                    yield r
            except OSError:
                continue

    def writer(self, params=None):
        params = self._mkparams(params)
        encoding = params["encoding"] if "encoding" in params else "utf-8"
        mode = params["mode"] if "mode" in params else "w"
        if "b" in mode:
            return self._location.open(mode)
        return self._location.open(mode, encoding=encoding)

    def path(self) -> str:
        return str(self._location.absolute())

    def child(self, subpath: str) -> 'Resource':
        return FileResource(self._location / subpath)

    def parent(self) -> 'Resource':
        return FileResource(self._location.parent)

    def is_dir(self) -> bool:
        return self._location.is_dir()

    def exists(self) -> bool:
        return self._location.exists()

    def mkdirs(self) -> None:
        self._location.mkdir()

    def ext(self) -> str:
        return self._location.suffix

    def basename(self) -> str:
        return self._location.name

    def descriptor(self) -> str:
        return self.path()


class StringResource(Resource):
    """
    Wraps a string as a resource
    """

    def __init__(self, string=""):
        self._buffer = string

    def reader(self, params=None):
        return io.StringIO(self._buffer)

    def writer(self, params=None):
        return io.StringIO()

    def write(self, content: str, params=None) -> None:
        with self.writer() as writer:
            writer.write(content)
            self._buffer = writer.getvalue()

    def read(self, params=None) -> str:
        if isinstance(self._buffer, bytes):
            params = self._mkparams(params)
            encoding = params["encoding"] if "encoding" in params else "utf-8"
            return self._buffer.decode(encoding)
        return self._buffer

    def path(self) -> str:
        return "string:"

    def descriptor(self) -> str:
        return "string:{}".format(self._buffer)

    def write_object(self, object):
        self._buffer = pickle.dumps(object)

    def read_object(self):
        return pickle.loads(self._buffer)


class UrlResource(Resource):
    """
    Wraps a url as resource
    """

    def writer(self, params=None):
        raise Exception("URL not writable")

    def __init__(self, url):
        self._url = url

    def reader(self, params=None):
        params = self._mkparams(params)
        timeout = params["timeout"] if "timeout" in params else 1000
        data = params["data"] if "data" in params else None
        return request.urlopen(self._url, timeout=timeout, data=data)

    def child(self, subpath: str) -> 'Resource':
        return UrlResource(request.urljoin(self._url, subpath))

    def parent(self) -> 'Resource':
        up = [x for x in urlparse.urlsplit(self._url)]
        p = Path(up[2]).parent
        up[2] = str(p)
        return UrlResource(urlparse.urlunsplit(up))

    def path(self) -> str:
        return self._url

    def ext(self) -> str:
        return splitext(self._url)[1]

    def basename(self) -> str:
        return Path(request.urlsplit(self._url)[2]).name

    def descriptor(self) -> str:
        return self.path()


__resource_creator = {
    "string:": lambda x: StringResource("" if x == "string:" else x[len("string:"):]),
    "http:": lambda x: UrlResource(x),
    "https:": lambda x: UrlResource(x)
}


def resource(path: Union[str, Resource]) -> 'Resource':
    if isinstance(path, Resource):
        return path
    for key in __resource_creator.keys():
        if path.startswith(key):
            return __resource_creator[key](path)
    return FileResource(path)
