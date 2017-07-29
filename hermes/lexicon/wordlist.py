import pygtrie as trie
import hermes.resource as res
from hermes.core import HString


class WordList:
    def __init__(self, case_insensitive=True):
        self._do_lower = case_insensitive

    def best_match(self, hstr):
        raise NotImplementedError

    def _convert(self, content):
        is_hstr = getattr(content, 'pos', None)
        if is_hstr:
            if self._do_lower:
                return content.lemma()
            return content.content
        return content.lower() if self._do_lower else content

    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __contains__(self, item):
        raise NotImplementedError

    def __iadd__(self, other):
        raise NotImplementedError

    def add(self, word):
        raise NotImplementedError

    def load(self, file):
        r = res.resource(file)
        for line in r.readlines():
            line = line.strip()
            if len(line) > 0 and line[0] != '#':
                self.add(line)

    def write(self, file):
        r = res.resource(file)
        with r.writer() as out_writer:
            for word in self:
                out_writer.write(word + '\n')


class SimpleWordList(WordList):
    def __init__(self, words=None, case_insensitive=True):
        super().__init__(case_insensitive)
        self._words = set(map(lambda w: w.lower() if case_insensitive else w, words if words else []))

    def __iadd__(self, other):
        self._words += other
        return self

    def best_match(self, hstr):
        if isinstance(hstr, HString):
            if hstr.content in self._words:
                return hstr.content
            elif hstr.lemma() in self._words:
                return hstr.lemma()
            elif self._do_lower and hstr.lower() in self._words:
                return hstr.lower()
        elif self._do_lower and hstr.lower() in self._words:
            return hstr.lower()
        elif hstr in self._words:
            return hstr
        return None

    def __iter__(self):
        return self._words.__iter__()

    def __len__(self):
        return len(self._words)

    def __contains__(self, item):
        return self._convert(item) in self._words

    def add(self, word):
        self._words.add(self._convert(word))


class PrefixSearchable:
    def is_prefix_match(self, item):
        raise NotImplementedError

    def prefixes(self, item):
        raise NotImplementedError


class TrieWordList(WordList, PrefixSearchable):
    def __init__(self, words=None, case_insensitive=True):
        super().__init__(case_insensitive)
        self._words = trie.CharTrie()
        for w in (words if words else []):
            self._words[self._convert(w)] = True

    def is_prefix_match(self, item):
        return self._words.has_subtrie(self._convert(item))

    def __iadd__(self, other):
        for w in other:
            self._words[self._convert(w)] = True
        return self

    def prefixes(self, item):
        return [w[0] for w in self._words.items(self._convert(item))]

    def __iter__(self):
        return iter(self._words)

    def __len__(self):
        return len(self._words)

    def __contains__(self, item):
        return self._convert(item) in self._words

    def add(self, word):
        self._words[self._convert(word)] = True


def longest_match_first(wl: WordList, hstr: HString, max_span=5):
    tkns = hstr.tokens()

    prefix_test = wl.is_prefix_match if isinstance(wl, PrefixSearchable) else lambda x: True
    tag_func = wl.tag if getattr(wl, 'tag', None) else lambda x: None

    for i in range(len(tkns)):
        tkn = tkns[i]
        if prefix_test(tkn) or tkn in wl:
            best_match = (tkn.start, tkn.end, wl._convert(tkn), 1, tag_func(tkn)) if tkn in wl else None

            for j in range(i, min(i + max_span, len(tkns))):
                tmp = HString.union(tkn, tkns[j])
                if tmp in wl:
                    best_match = (tkn.start, tkns[j].end, wl._convert(tmp), j - i + 1, tag_func(tmp))

                if not prefix_test(tmp):
                    break

            if best_match:
                yield best_match
                i += best_match[3]


def prefix_find_all(wl: PrefixSearchable, content: str):
    cl = len(content)
    start = 0
    lm = -1
    key = ''
    for i in range(cl):
        key += content[i]
        if key in wl:
            nextI = lm = i + 1
            if nextI < cl and wl.is_prefix_match(key + content[i + 1]):
                continue
            lm = -1
            yield (start, nextI, content[start:nextI], key)
            start = nextI
            key = ''
        elif not not wl.is_prefix_match(key):
            if lm != -1:
                nextI = lm
                lm = -1
                yield (start, nextI, content[start:nextI])
                start = nextI
                key = ''
            else:
                start = i + 1
                key = ''
