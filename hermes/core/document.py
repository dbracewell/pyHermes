import json
import typing
from collections import OrderedDict
from random import randint
import hermes.language as lng
from hermes.core.attributes import get_decoder
from hermes.core.preprocess import preprocess
from hermes.types import LANGUAGE
from .annotation import Annotation
from .hstring import HString
from quicksect import IntervalTree, Interval


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
        self._completed = set()
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
        annotation_type = annotation_type.lower()
        try:
            if end is None or start is None:
                anno_iter = self._annotations.find(Interval(0, self.end))
            else:
                anno_iter = self._annotations.find(Interval(start, end))
        except Exception:
            return []
        return sorted(
            [x.data for x in anno_iter if x.data.annotation_type.lower() == annotation_type and x.data != self])

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
        # self._annotations.addi(annotation.start, annotation.end, annotation)
        self._annotations.add(annotation.start, annotation.end, annotation)
        # self._annotations[annotation.start:annotation.end] = annotation
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
                self._completed.add(arg)
            else:
                raise Exception("No annotator for {} annotations in {}".format(arg, self.language()))

    def language(self):
        if LANGUAGE in self.attributes:
            return self.attributes[LANGUAGE]
        return lng.UNKNOWN

    @staticmethod
    def from_json(json_str):
        obj = json.loads(json_str)
        doc = Document(obj["content"], doc_id=obj["id"])
        for (k, v) in obj["attributes"].items():
            doc[k] = get_decoder(k)(v)
        if "annotations" in obj:
            for annotation in obj["annotations"]:
                ann = Annotation(
                    document=doc,
                    start=annotation["start"],
                    end=annotation["end"],
                    annotation_type=annotation["type"],
                    attributes=[(k, get_decoder(k)(v)) for k, v in annotation["attributes"].items()],
                    annotation_id=annotation["id"]
                )
                doc._annotations.add(ann.start, ann.end, ann)
                if "relations" in obj["annotations"]:
                    for rel in obj["annotations"]:
                        ann.add_relation(target=rel["target"], type=rel["type"], relation=rel["value"])
        doc.language().load()
        return doc

    def to_json(self) -> str:
        aout = []
        try:
            aout = self._annotations.find(0, self.length)
        except Exception:
            aout = []
        return json.dumps(OrderedDict([("id", self._doc_id),
                                       ("content", self.content),
                                       ("attributes", self._attributes),
                                       ("annotations", [a.as_dict() for a in aout])],
                                      default=default))
