from .hstring import HString
from .relation import Relation


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
