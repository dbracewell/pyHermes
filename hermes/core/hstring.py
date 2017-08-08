import re
import typing
from collections import defaultdict

import hermes.language as lng
from hermes.tag.pos import PartOfSpeech
from hermes.types import TOKEN, PART_OF_SPEECH, LANGUAGE
from .span import Span


def return_none():
    """
    Simple method that returns None for defaultdict to allow pickling
    :return:  None
    """
    return None


class HString(Span):
    """

    """

    def __init__(self, document: 'Document', start: int, end: int) -> None:
        super(HString, self).__init__(start, end)
        self._document = document
        self._attributes = defaultdict(return_none)
        self._tokens = []

    def is_empty(self):
        return self.start == self.end

    def __len__(self):
        return len(self._document.content)

    def __lt__(self, other):
        return self.start < other.start or (self.start == other.start and self.end < other.end)

    @property
    def content(self) -> str:
        return self._document.content[self.start:self.end] if self._document and not self.is_empty() else ""

    def __contains__(self, item) -> bool:
        return item in self._attributes

    def __getitem__(self, attribute) -> typing.Any:
        """
        Gets the value of the given attribute
        :param attribute: The attribute whose value should be returned
        :return: The value of the attribute or None if the attribute is not present
        """
        if isinstance(attribute, slice):
            return HString(self, attribute.start, attribute.stop)
        if attribute in self._attributes:
            return self._attributes[attribute]
        return None

    def __setitem__(self, attribute, value) -> None:
        """
        Sets the value of the given the attribute on this HString
        :param attribute: The attribute to set
        :param value:  The value of the attribute
        :return: None
        """
        if value is None:
            if attribute in self._attributes:
                del self._attributes[attribute]
        else:
            self._attributes[attribute] = value

    def __delitem__(self, key) -> typing.Any:
        del (self._attributes[key])

    def __getslice__(self, i, j):
        return HString(self._document, i, j)

    def __unicode__(self) -> str:
        return self.content

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        return self.content

    def has(self, attribute):
        return attribute in self._attributes

    @staticmethod
    def union(*hstr):
        if hstr:
            start = min(hstr).start
            end = max(hstr).end
            return HString(hstr[0].document, start, end)
        return HString(None, 0, 0)

    def token_length(self):
        return len(self.tokens())

    def lemma(self):
        if 'lemma' in self._attributes:
            return self['lemma']
        tkn = self.tokens()
        if len(tkn) == 0:
            return self.lower()
        return " ".join([t.lemma() for t in tkn])

    def is_stopword(self) -> bool:
        return self.language().is_stopword(self)

    def language(self) -> lng.Language:
        if LANGUAGE in self._attributes:
            return self._attributes[LANGUAGE]
        return self._document.language() if self._document else lng.UNKNOWN

    def rstrip(self, stripper=lambda x: x.is_stopword()):
        if self.is_empty():
            return self
        for tkn in reversed(self.tokens()):
            if not stripper(tkn):
                return HString(self.document, self.start, tkn.end)
        return HString(None, 0, 0)

    def lstrip(self, stripper=lambda x: x.is_stopword()):
        if self.is_empty():
            return self
        for tkn in self.tokens():
            if not stripper(tkn):
                return HString(self.document, tkn.start, self.end)
        return HString(None, 0, 0)

    def strip(self, stripper=lambda x: x.is_stopword()):
        ls = self.lstrip(stripper)
        return ls.rstrip(stripper) if len(ls.tokens()) > 1 else ls

    def find(self, string, start=0) -> 'HString':
        idx = self.content.find(string, start)
        if idx >= 0:
            return HString(self._document, idx, idx + len(string))
        return HString(None, 0, 0)

    def re_find(self, pattern, start=0) -> 'HString':
        if isinstance(pattern, str):
            regex = re.compile(pattern)
            r = regex.search(self.content, start)
        else:
            r = pattern.search(self.content, start)
        if r:
            return HString(self._document, r.start(), r.end())
        return HString(None, 0, 0)

    def annotation(self, annotation_type) -> typing.List['Annotation']:
        return self._document.annotation(annotation_type, start=self.start, end=self.end) if self._document else []

    @property
    def document(self) -> 'Document':
        return self._document

    def pos(self) -> PartOfSpeech:
        p = self[PART_OF_SPEECH]
        return p if p else PartOfSpeech.guess(self)

    def tokens(self) -> typing.List['Annotation']:
        if not self._tokens:
            self._tokens = self.annotation(TOKEN)
        return self._tokens

    @property
    def attributes(self) -> typing.Dict[str, typing.Any]:
        return self._attributes

    def lower(self) -> str:
        return self.content.lower()

    def upper(self) -> str:
        return self.content.upper()
