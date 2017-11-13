import sys
from collections import namedtuple

from hermes.core import Document

sys.path.append("/home/dbb/PycharmProjects/hermes-py/")
from hermes.resource import resource
from hermes.util import Timer
import json


# r = resource('/home/dbb/annotated2.json_opl')
# timer = Timer(started=True)
# with r.reader() as rdr:
#     for line in rdr:
#         if len(line.strip()) > 0:
#             Document.from_json(line)
# print(timer)


#


doc = Document('Hi   how\n  are you?');
doc.annotate('token')
for tok in doc.tokens():
    print(tok, tok.pos())


# class SSpan(namedtuple('SSpan', 'start end')):
#     __slots__ = ()
#
#     def overlaps(self, other):
#         return self.start < other.end and self.end > other.start
#
#
# class SDoc(SSpan):
#     def __new__(cls, content, document_id="1"):
#         # def __init__(self, content, document_id="1"):
#         self = super(SDoc, cls).__new__(cls, start=0, end=len(content))
#         # super().__init__(0, len(content))
#         self.content = content
#         self.document_id = document_id
#         self.annotations = []
#         self.attributes = {}
#         self.completed = {}
#         return self
#
#
# class HString(SSpan):
#     def __new__(cls, owner, start, end):
#         self = super(HString, cls).__new__(cls, start, end)
#         self.owner = owner
#         self.attributes = {}
#         return self
#
#     def lower(self):
#         return str(self).lower()
#
#     def upper(self):
#         return str(self).upper()
#
#     def overlapping(self, annotation_type):
#         return filter(lambda a: a.annotation_type == annotation_type and self.overlaps(a), self.owner.annotations)
#
#     def __str__(self):
#         return self.owner.content[self.start:self.end]
#
#     def __repr__(self) -> str:
#         return self.owner.content[self.start:self.end]
#
#
# class Annotation(HString):
#     def __new__(cls, owner, annotation_type, annotation_id, start, end):
#         self = super(Annotation, cls).__new__(cls, owner, start, end)
#         self.annotation_type = annotation_type
#         self.annotation_id = annotation_id
#         self.relations = []
#         return self
#
#
# class Relation(namedtuple('Relation', 'document source target relation relation_type')):
#     def __repr__(self) -> str:
#         return "(source={}, target={}, type={}, relation={})".format(self.source, self.target, self.relation_type,
#                                                                      self.relation)
#
#     @property
#     def source(self):
#         return self.document.annotation_by_id(self.source)
#
#     @property
#     def target(self):
#         return self.document.annotation_by_id(self.target)
#
#
# from hermes.core.attributes import get_decoder
#
# timer = Timer(started=True)
# r = resource('/home/dbb/annotated2.json_opl')
#
#
# def convert(line):
#     obj = json.loads(line)
#     doc = SDoc(content=obj['content'], document_id=obj.get('id', '1'))
#     for (k, v) in obj.get("attributes", {}).items():
#         doc.attributes[k] = get_decoder(k)(v)
#     for (k, v) in obj.get('completed', {}).items():
#         doc.completed[k] = v
#     max_id = -1
#     for annotation in obj.get("annotations", []):
#         ann = Annotation(
#             owner=doc,
#             start=annotation["start"],
#             end=annotation["end"],
#             annotation_type=annotation["type"],
#             annotation_id=annotation["id"]
#         )
#         doc.annotations.append(ann)
#         max_id = max(max_id, ann.annotation_id)
#         doc.attributes['max_annotation_id'] = max_id
#         ann.attributes = dict([(k, get_decoder(k)(v)) for k, v in annotation.get("attributes", {}).items()])
#         for rel in annotation.get("relations", []):
#             ann.relations.append(
#                 Relation(document=doc, source=ann.annotation_id, target=rel["target"],
#                          relation_type=rel["type"], relation=rel["value"]))
#     return doc
#
#
# from collections import defaultdict
#
# counts = defaultdict(int)
# generator = r.children(recursive=True, pattern="*.*", include_dirs=False) if r.is_dir() else [r]
# for file in generator:
#     with file.reader() as rdr:
#         for line in rdr:
#             if len(line.strip()) > 0:
#                 doc = convert(line)
#                 for pc in filter(
#                         lambda x: x.annotation_type == 'phrase_chunk',
#                         doc.annotations):
#                     counts[pc.lower()] += 1
# print(timer)
#
# # from collections import Counter
# #
# # counts = Counter(counts)
# # print(counts.most_common(10))
