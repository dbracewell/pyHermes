import json
import typing
from quicksect import Interval, IntervalTree
from random import randint
import hermes.language as lng
from hermes.core.attributes import get_decoder
from hermes.core.preprocess import preprocess
from hermes.types import LANGUAGE
from .annotation import Annotation
from .hstring import HString
from .span import Span

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


def rand_id(length: int = 10) -> str:
    """
    Generates a random length string id where each character is in the range a-z or 0-9
    :param length: Length of the random id
    :return: Random id
    """
    character_range = "abcdefghijklmnopqrstuvwxyz0123456789"
    out = ""
    while len(out) < length:
        out += character_range[randint(0, len(character_range) - 1)]
    return out


def default(o):
    return str(o)


class Document(HString):
    def __init__(self, content, doc_id=rand_id(), language=lng.ENGLISH, preprocessors=None):
        super().__init__(self, 0, len(content))
        self._content = preprocess(content, preprocessors) if preprocessors else content
        self._annotations = IntervalTree()
        self._doc_id = rand_id(10) if doc_id is None else doc_id
        self._completed = {}
        self._next_id = 0
        self[LANGUAGE] = language
        self._aid_dict = {}

    @property
    def content(self) -> str:
        return self._content

    @property
    def doc_id(self):
        return self._doc_id

    def annotation(self, annotation_type, start=None, end=None) -> typing.List[Annotation]:
        try:
            if end is None or start is None:
                anno_iter = self._annotations.find(Interval(0, self.end))
            else:
                anno_iter = filter(lambda x: x.data.overlaps(Span(start, end))
                                   , self._annotations.find(Interval(start, end)))
        except:
            return []
        if annotation_type:
            annotation_type = annotation_type.lower()
            return sorted(
                [x.data for x in anno_iter if x.data.annotation_type.lower() == annotation_type and x.data != self])
        return sorted([x.data for x in anno_iter if x.data != self])

    def annotation_by_id(self, annotation_id: int):
        return self._aid_dict[annotation_id] if annotation_id in self._aid_dict else None

    def previous_annotation(self, annotation: Annotation, annotation_type: str = None) -> 'Annotation':
        if not annotation_type:
            annotation_type = annotation.annotation_type
        a = self.annotation(annotation_type, start=-1, end=annotation.start)
        if len(a) == 0:
            return Annotation(None, 0, 0, annotation_type, [])
        return a[-1]

    def next_annotation(self, annotation: Annotation, annotation_type: str = None) -> 'Annotation':
        if not annotation_type:
            annotation_type = annotation.annotation_type
        a = self.annotation(annotation_type, start=annotation.end, end=self.end)
        if len(a) == 0:
            return Annotation(None, 0, 0, annotation_type, [])
        return a[0]

    def create_annotation(self, type: str, start: int, end: int, attributes=None) -> Annotation:
        if attributes is None:
            attributes = []
        annotation = Annotation(self, start, end, type, attributes, self._next_id)
        self._next_id += 1
        self._annotations.insert(Interval(annotation.start, annotation.end, annotation))
        self._aid_dict[annotation.annotation_id] = annotation
        return annotation

    def annotate(self, *args):
        for arg in args:
            if arg in self._completed:
                continue
            self.language().load()
            annotator = self.language().get_annotator(arg)
            if annotator:
                annotator.annotate(self)
                self._completed[arg] = '1.0'
            else:
                raise Exception("No annotator for {} annotations in {}".format(arg, self.language()))

    def language(self):
        if LANGUAGE in self.attributes:
            return self.attributes[LANGUAGE]
        return lng.UNKNOWN

    @staticmethod
    def from_json(json_str):
        doc = Document(content='')
        doc.__read_json(json.loads(json_str))
        return doc

    def __getstate__(self):
        return self.to_dict()

    def __setstate__(self, state):
        self.__read_json(state)

    def __read_json(self, obj):
        self.__init__(content=obj['content'])
        if "id" in obj:
            self._doc_id = obj["id"]
        if 'attributes' in obj:
            for (k, v) in obj["attributes"].items():
                self[k] = get_decoder(k)(v)
        if 'completed' in obj:
            for (k, v) in obj['completed'].items():
                self._completed[k] = v
        max_id = -1
        if "annotations" in obj:
            for annotation in obj["annotations"]:
                ann = Annotation(
                    document=self,
                    start=annotation["start"],
                    end=annotation["end"],
                    annotation_type=annotation["type"],
                    attributes=[(k, get_decoder(k)(v)) for k, v in annotation["attributes"].items()],
                    annotation_id=annotation["id"]
                )
                max_id = max(max_id, ann.annotation_id)
                self._annotations.add(ann.start, ann.end, ann)
                if "relations" in obj["annotations"]:
                    for rel in obj["annotations"]:
                        ann.add_relation(target=rel["target"], type=rel["type"], relation=rel["value"])
        self.language().load()
        self._next_id = max_id + 1

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=default)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return dict([("id", self._doc_id),
                     ("content", self.content),
                     ("attributes", self._attributes),
                     ("completed", self._completed),
                     ("annotations", [a.as_dict() for a in self.annotation(annotation_type=None)])])
