class Tag:
    def __init__(self, parent: 'Tag' = None):
        self._parent = parent

    def is_a(self, other: [str, 'Tag']):
        me = self
        target = other.upper() if isinstance(other, str) else other.name
        while me is not None:
            if me.name == target:
                return True
            me = me.parent
        return False

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, o: object) -> bool:
        return isinstance(o, 'Tag') and self.name == o.name

    @property
    def parent(self) -> 'Tag':
        return self._parent

    @property
    def name(self) -> str:
        raise NotImplementedError
