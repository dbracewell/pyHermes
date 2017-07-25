from .timer import Timer
import typing

__all__ = ["Timer"]


def to_lower(d: typing.Dict[str, typing.Any]):
    if d:
        return dict([(k.lower(), v) for k, v in d.items()])
    return {}
