from .wordlist import WordList, PrefixSearchable
import pygtrie as trie
from hermes.resource import resource
import csv


class Lexicon(WordList, PrefixSearchable):
    def __init__(self, tuples=None, case_insensitive=True):
        super().__init__(case_insensitive)
        self._words = trie.CharTrie()
        for word, tag in (tuples if tuples else []):
            self._words[self._convert(word)] = tag

    def load(self, file, tag_decoder=lambda x: x):
        for line in resource(file).readlines():
            row = line.split(',')
            if len(row) >= 2:
                self.add(row[0].strip(), tag_decoder(row[1].strip()))

    def is_prefix_match(self, item):
        return self._words.has_subtrie(self._convert(item))

    def tag(self, item):
        c = self._convert(item)
        return self._words[c] if c in self._words else None

    def __iadd__(self, other):
        for w in other:
            self._words[self._convert(w)] = other.tag(w)
        return self

    def prefixes(self, item):
        return [w[0] for w in self._words.items(self._convert(item))]

    def __iter__(self):
        return iter(self._words)

    def __len__(self):
        return len(self._words)

    def __contains__(self, item):
        return self._convert(item) in self._words

    def add(self, word, tag=None):
        self._words[self._convert(word)] = tag
