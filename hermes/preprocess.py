import re
from typing import List, Callable
import html.entities
import unicodedata

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

__ws = re.compile("[ \t]+")
__nl = re.compile("(?:\r?\n)+")
__nl_ws = re.compile("\n[ \t]")
__html_entity = re.compile(r"&(?:(?:#\d+)|(?:\w+));")
__html_tag = re.compile(r"<[^>]+>")

__preprocessors = {
    "whitespace": lambda x: __nl_ws.sub('\n', __ws.sub(' ', x.strip())),
    "newline": lambda x: __nl.sub('\n', x),
    "html_entity": lambda x: __html2unicode(x),
    "unicode": lambda x: unicodedata.normalize('NFKC', x),
    "html_tag": lambda x: __html_tag.sub('', x)
}


def __html2unicode(s):
    for entity in set(__html_entity.findall(s)):
        try:
            num = int(entity[2:-1])
            s = s.replace(entity, chr(num))
            continue
        except ValueError:
            name = entity[1:-1]
            if name in html.entities.name2codepoint:
                s = s.replace(entity, chr(html.entities.name2codepoint[name]))
    return s


def add_preprocessor(name: str, func: Callable):
    __preprocessors[name.lower()] = func


def valid_preprocessors() -> List[str]:
    return list(__preprocessors.keys())


def preprocess(content: str, preprocessors: List[str]):
    for p in preprocessors:
        p = p.lower()
        if p in __preprocessors:
            content = __preprocessors[p](content)
    return content
