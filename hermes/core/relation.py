
class Relation(object):
    def __init__(self, document, source: int, target: int, relation: str, relation_type: str):
        self._document = document
        self._source = source
        self._target = target
        self._relation = relation
        self._type = relation_type

    def __repr__(self) -> str:
        return "(source={}, target={}, type={}, relation={})".format(self.source, self.target, self._type,
                                                                     self._relation)

    @property
    def source(self):
        return self._document.annotation_by_id(self._source)

    @property
    def target(self):
        return self._document.annotation_by_id(self._target)

    @property
    def relation_type(self):
        return self._type

    @property
    def relation(self):
        return self._relation