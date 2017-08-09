from .hstring import HString
from .relation import Relation

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


class Annotation(HString):
    def __init__(self, document, start: int, end: int, annotation_type: str, attributes=None, annotation_id=-1):
        super().__init__(document, start, end)
        self._type = annotation_type
        self._relations = []
        self._id = annotation_id
        if attributes is None:
            attributes = []
        if isinstance(attributes, list):
            for k, v in attributes:
                self[k] = v
        else:
            for k, v in attributes.items():
                self[k] = v

    def tokens(self):
        if self._type == 'token':
            return [self]
        return super().tokens()

    def head(self) -> 'Annotation':
        rel = next(filter(lambda x: x.relation_type == 'dep', self._relations), None)
        if rel:
            return rel.target
        return Annotation(None, 0, 0, 'token')

    def add_relation(self, target: ['Annotation', int], type: str, relation: str):
        target_id = target if isinstance(target, int) else target["id"]
        rel = Relation(self.document, self["id"], target_id, relation, type)
        self._relations.append(rel)

    def next(self, annotation_type=None) -> 'Annotation':
        return self.document.next_annotation(self, annotation_type)

    def previous(self, annotation_type=None) -> 'Annotation':
        return self.document.previous_annotation(self, annotation_type)

    def as_dict(self):
        dd = {"type": self._type,
              "start": self.start,
              "end": self.end,
              "id": self.annotation_id,
              "attributes": self.attributes}
        if len(self._relations) > 0:
            dd["relations"] = [{"target": rel.target.annotation_id,
                                "type": rel.relation_type,
                                "value": rel.relation} for rel in self._relations]
        return dd

    @property
    def relations(self):
        return self._relations

    @property
    def annotation_type(self):
        return self._type

    @property
    def annotation_id(self):
        return self._id
