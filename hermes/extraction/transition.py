from .nfa import NFA, Transition
from hermes.types import PART_OF_SPEECH

class StopWordTransition(Transition):
    def matches(self, hStr) -> int:
        return hStr.token_length() if hStr.is_stopword() else 0

    def __str__(self) -> str:
        return '${STOPWORD}'

    def __repr__(self) -> str:
        return str(self)

    def not_matches(self, hStr) -> int:
        return 0 if hStr.is_stopword() else hStr.token_length()

    @staticmethod
    def create(word):
        return StopWordTransition()


class TagTransition(Transition):
    def __init__(self, tag):
        self.__to_match = tag

    def matches(self, hStr) -> int:
        tl = hStr.token_length()
        if PART_OF_SPEECH in hStr:
            return tl if hStr[PART_OF_SPEECH].is_a(self.__to_match) else 0
        elif 'tag' in hStr:
            return tl if hStr['tag'] == self.__to_match else 0
        return 0

    def __str__(self) -> str:
        return '#%s' % self.__to_match

    def __repr__(self) -> str:
        return str(self)

    def not_matches(self, hStr) -> int:
        return hStr.token_length() - self.matches(hStr)

    @staticmethod
    def create(word):
        return TagTransition(tag=word[1:])


class AttributeTransition(Transition):
    def __init__(self, attribute, value):
        self.__attribute = attribute
        self.__value = value

    def matches(self, hStr) -> int:
        from hermes.util import eq_to_str
        tl = hStr.token_length()
        if self.__attribute in hStr:
            return tl if eq_to_str(hStr[self.__attribute], self.__value) else 0
        return 0

    def __str__(self) -> str:
        return '#{%s: %s}' % (self.__attribute, self.__value)

    def __repr__(self) -> str:
        return str(self)

    def not_matches(self, hStr) -> int:
        return hStr.token_length() - self.matches(hStr)

    @staticmethod
    def create(word):
        word = word[2:-1]
        idx = word.find(':')
        return AttributeTransition(attribute=word[:idx].strip(), value=word[idx + 1:].strip())


class NumberTransition(Transition):
    def __init__(self):
        import regex as re
        self.__number_pattern = re.compile('(\d{1,3}([.,]\d{3})*([,.]\d+)?|[.,]\d+)', re.UNICODE)

    def matches(self, hStr) -> int:
        tl = hStr.token_length()
        if self.__number_pattern.fullmatch(hStr.content):
            return tl
        return 0

    def __str__(self) -> str:
        return '${NUMBER}'

    def __repr__(self) -> str:
        return str(self)

    def not_matches(self, hStr) -> int:
        return hStr.token_length() - self.matches(hStr)

    @staticmethod
    def create(word):
        return NumberTransition()


class PunctTransition(Transition):
    def __init__(self):
        import regex as re
        self.__punct_pattern = re.compile('\p{P}', re.UNICODE)

    def matches(self, hStr) -> int:
        tl = hStr.token_length()
        if self.__punct_pattern.fullmatch(hStr.content):
            return tl
        return 0

    def __str__(self) -> str:
        return '${PUNCT}'

    def __repr__(self) -> str:
        return str(self)

    def not_matches(self, hStr) -> int:
        return hStr.token_length() - self.matches(hStr)

    @staticmethod
    def create(word):
        return PunctTransition()


class WordTransition(Transition):
    @staticmethod
    def create(word):
        lemmatize = False
        case_insensitive = False
        if word.endswith(")"):
            s = len(word) - 2
            while s >= 0 and word[s] != '(':
                s -= 1
            options = word[s + 2:-1].lower()
            lemmatize = 'l' in options
            case_insensitive = 'i' in options
            word = word[0:s]
        word = word.replace('\\', "")
        return WordTransition(word, lemmatize=lemmatize, case_insensitive=case_insensitive)

    def __init__(self, to_match, lemmatize=False, case_insensitive=False):
        self.case_insensitive = case_insensitive
        self.lemmatize = lemmatize
        self._to_match = to_match

    def __str__(self) -> str:
        out = self._to_match
        if self.lemmatize:
            out += '(?l)'
        elif self.case_insensitive:
            out += '(?i)'
        return out

    def __repr__(self) -> str:
        return str(self)

    def not_matches(self, hStr) -> int:
        return hStr.token_length() - self.matches(hStr)

    def matches(self, hStr) -> int:
        if hStr.content == self._to_match:
            return hStr.token_length()
        elif self.lemmatize and hStr.lemma() == self._to_match:
            return hStr.token_length()
        elif self.case_insensitive and hStr.lower() == self._to_match.lower():
            return hStr.token_length()
        return 0


class RegexTransition(Transition):
    @staticmethod
    def create(word):
        word = word[1:]
        lemmatize = False
        case_insensitive = False
        if word.endswith("/"):
            word = word[:-1]
        else:
            lemmatize = word.endswith("l")
            case_insensitive = word.endswith("i")
            word = word[:-2]
        word = word.replace('\\', "").strip()
        return RegexTransition(word, lemmatize=lemmatize, case_insensitive=case_insensitive)

    def __init__(self, to_match, lemmatize=False, case_insensitive=False):
        import regex as re
        self.case_insensitive = case_insensitive
        self.lemmatize = lemmatize
        self._to_match = to_match
        if self.case_insensitive:
            self._pattern = re.compile(to_match, re.I)
        else:
            self._pattern = re.compile(to_match)

    def __str__(self) -> str:
        out = '/' + self._to_match + '/'
        if self.lemmatize:
            out += '(?l)'
        elif self.case_insensitive:
            out += '(?i)'
        return out

    def __repr__(self) -> str:
        return str(self)

    def not_matches(self, hStr) -> int:
        return hStr.token_length() - self.matches(hStr)

    def matches(self, hStr) -> int:
        if self._pattern.search(hStr.content):
            return hStr.token_length()
        elif self.lemmatize and self._pattern.search(hStr.lemma()):
            return hStr.token_length()
        return 0


class NotTransition(Transition):
    def __init__(self, sub_exp):
        self._sub_exp = sub_exp

    def __str__(self) -> str:
        return '^(%s)' % self._sub_exp

    def __repr__(self) -> str:
        return str(self)

    def matches(self, hStr) -> int:
        return self._sub_exp.not_matches(hStr)

    def not_matches(self, hStr) -> int:
        return self._sub_exp.matches(hStr)


class SequenceTransition(Transition):
    def __init__(self, sub_exp):
        self._sub_exp = sub_exp

    def __str__(self) -> str:
        return '(%s)' % ' '.join(map(lambda x: str(x), self._sub_exp))

    def __repr__(self) -> str:
        return str(self)

    def matches(self, hStr) -> int:
        l = 0
        for sub in self._sub_exp:
            t = sub.matches(hStr)
            if hStr.is_empty():
                l = 0
                break
            if not hStr.is_empty() and t > 0:
                l += t
                while t > 0:
                    hStr = hStr.next()
                    t -= 1
            else:
                l = 0
                break
        return l

    def not_matches(self, hStr) -> int:
        l = 0
        for sub in self._sub_exp:
            if hStr.is_empty():
                l = 0
                break
            t = sub.not_matches(hStr)
            if t > 0:
                l += t
                while not hStr.is_empty() and t > 0:
                    hStr = hStr.next()
                    t -= 1
            else:
                l = 0
                break
        return l

    def construct(self) -> NFA:
        nfa = NFA()
        nfa.start.connect(nfa.end)
        for sub in self._sub_exp:
            other = sub.construct()
            nfa.end.accept = False
            nfa.end.connect(other.end, sub)
            nfa.end = other.end
        return nfa


class GroupTransition(SequenceTransition):
    def __init__(self, sub_exp, name):
        super().__init__(sub_exp)
        self._name = name

    def __str__(self) -> str:
        return '(?<%s> %s)' % (self._name, ' '.join(map(lambda x: str(x), self._sub_exp)))

    def __repr__(self) -> str:
        return str(self)

    def construct(self) -> NFA:
        nfa = NFA()
        nfa.start.connect(nfa.end)
        nfa.start.emits = True
        nfa.start.name = self._name

        for sub in self._sub_exp:
            other = sub.construct()
            nfa.end.accept = False
            nfa.end.connect(other.end, sub)
            nfa.end = other.end

        nfa.end.isAccept = True
        nfa.end.consumes = True
        nfa.end.name = self._name

        return nfa


class AnyTransition(Transition):
    def matches(self, hStr) -> int:
        return hStr.token_length()

    def not_matches(self, hStr) -> int:
        return 0

    def __str__(self) -> str:
        return "~"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def create(word):
        return AnyTransition()


class ZeorOrOne(Transition):
    def __init__(self, sub):
        self._sub = sub

    def matches(self, hStr) -> int:
        return hStr.token_length() if self._sub.matches(hStr) else 1

    def __str__(self) -> str:
        return '(%s?)' % self._sub

    def __repr__(self) -> str:
        return str(self)

    def not_matches(self, hStr) -> int:
        return hStr.token_length() if not self._sub.matches(hStr) else 1
