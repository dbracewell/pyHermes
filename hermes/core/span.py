
class Span(object):
    """
        Represents a contiguous range of characters, i.e. a start and an end.
    """

    def __str__(self) -> str:
        return "({}, {})".format(self._start, self._end)

    def __init__(self, start: int, end: int) -> None:
        self._start = start
        self._end = end

    @property
    def start(self) -> int:
        """
        Character starting offset
        :return: start character offset
        """
        return self._start

    @property
    def end(self) -> int:
        """
        Character ending offset
        :return:  end character offset
        """
        return self._end

    @property
    def length(self) -> int:
        """
        Length of span
        :return: span length
        """
        return self.end - self.start

    def overlaps(self, other: 'Span') -> bool:
        """
        Determines if this span overlaps with another
        :param other: The other span
        :return: True if this span overlaps the other, False otherwise
        """
        return isinstance(other, Span) and self.start < other.end and self.end > other.start
