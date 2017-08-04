from .timer import Timer
import typing

__all__ = ["Timer"]


def to_lower(d: typing.Dict[str, typing.Any]):
    if d:
        return dict([(k.lower(), v) for k, v in d.items()])
    return {}


def eq_to_str(o1, o2: str):
    from hermes.tag import Tag
    try:
        if isinstance(o1, str):
            return o1 == o2
        elif isinstance(o1, int) \
                or isinstance(o1, float):
            return o1 == float(o2)
        elif isinstance(o1, Tag):
            return o1.is_a(o2)
    except:
        pass
    return False
