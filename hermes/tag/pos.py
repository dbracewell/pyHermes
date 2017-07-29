"""
   Copyright 2017 David B. Bracewell

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from .tag import Tag

_lookup = {}


class PartOfSpeech(Tag):
    def __init__(self, tag: str, coarse=None):
        super().__init__(parent=coarse)
        tag = tag.upper()
        if tag in _lookup:
            raise Exception("{0} is already defined".format(tag))
        _lookup[tag] = self
        self._tag = tag

    def is_noun(self):
        return self.is_a(Universal.NOUN)

    def is_verb(self):
        return self.is_a(Universal.VERB)

    def is_adjective(self):
        return self.is_a(Universal.ADJECTIVE)

    def is_adverb(self):
        return self.is_a(Universal.ADVERB)

    def is_pronoun(self):
        return self.is_a(Universal.PRONOUN)

    def is_particle(self):
        return self.is_a(Universal.PARTICLE)

    def is_adposition(self):
        return self.is_a(Universal.ADPOSITION)

    def is_conjunction(self):
        return self.is_a(Universal.CONJUNCTION)

    def is_determiner(self):
        return self.is_a(Universal.DETERMINER)

    def is_number(self):
        return self.is_a(Universal.NUMBER)

    def is_unknown(self):
        return self.is_a(Universal.UNKNOWN)

    def is_other(self):
        return self.is_a(Universal.OTHER)

    @staticmethod
    def guess(hs: 'HString'):
        if hs is None:
            return Universal.UNKNOWN
        if hs.has('pos'):
            return hs['pos']
        hs = hs.head()
        return hs.pos()

    @staticmethod
    def of(tag):
        tag = tag.upper()
        if tag in _lookup:
            return _lookup[tag]
        return Universal.UNKNOWN

    def __repr__(self) -> str:
        return self._tag

    def __eq__(self, other):
        if isinstance(other, PartOfSpeech):
            return self._tag == other._tag
        return False

    @property
    def name(self):
        return self._tag


class Universal:
    UNKNOWN = PartOfSpeech("ANY")
    NOUN = PartOfSpeech("NOUN")
    VERB = PartOfSpeech("VERB")
    PUNCTUATION = PartOfSpeech("PUNCTUATION")
    PRONOUN = PartOfSpeech("PRON")
    ADJECTIVE = PartOfSpeech("ADJ")
    ADVERB = PartOfSpeech("ADV")
    ADPOSITION = PartOfSpeech("ADP")
    CONJUNCTION = PartOfSpeech("CONJ")
    DETERMINER = PartOfSpeech("DET")
    NUMBER = PartOfSpeech("NUM")
    PARTICLE = PartOfSpeech("PRT")
    OTHER = PartOfSpeech("X")


class PennTreebank:
    NN = PartOfSpeech("NN", Universal.NOUN)
    NNP = PartOfSpeech("NNP", Universal.NOUN)
    NNS = PartOfSpeech("NNS", Universal.NOUN)
    NNPS = PartOfSpeech("NNPS", Universal.NOUN)
    NP = PartOfSpeech("NP", Universal.NOUN)
    VP = PartOfSpeech("VP", Universal.VERB)
    VB = PartOfSpeech("VB", Universal.VERB)
    VBD = PartOfSpeech("VBD", Universal.VERB)
    VBG = PartOfSpeech("VBG", Universal.VERB)
    VBN = PartOfSpeech("VBN", Universal.VERB)
    VBP = PartOfSpeech("VBP", Universal.VERB)
    VBZ = PartOfSpeech("VBZ", Universal.VERB)
    ADJP = PartOfSpeech("ADJP", Universal.ADVERB)
    SBAR = PartOfSpeech("SBAR", Universal.OTHER)
    CONJP = PartOfSpeech("CONJP", Universal.CONJUNCTION)
    INTJ = PartOfSpeech("INT", Universal.OTHER)
    LST = PartOfSpeech("LST", Universal.OTHER)
    UCP = PartOfSpeech("UCP", Universal.OTHER)
    CC = PartOfSpeech("CC", Universal.CONJUNCTION)
    CD = PartOfSpeech("CD", Universal.NUMBER)
    DT = PartOfSpeech("DT", Universal.DETERMINER)
    EX = PartOfSpeech("EX", Universal.DETERMINER)
    FW = PartOfSpeech("FW", Universal.OTHER)
    IN = PartOfSpeech("IN", Universal.ADPOSITION)
    JJ = PartOfSpeech("JJ", Universal.ADJECTIVE)
    JJR = PartOfSpeech("JJR", Universal.ADJECTIVE)
    JJS = PartOfSpeech("JJS", Universal.ADJECTIVE)
    LS = PartOfSpeech("LS", Universal.OTHER)
    MD = PartOfSpeech("MD", Universal.VERB)
    PDT = PartOfSpeech("PDT", Universal.DETERMINER)
    POS = PartOfSpeech("POS", Universal.PARTICLE)
    PRP = PartOfSpeech("PRP", Universal.PRONOUN)
    PRP_POS = PartOfSpeech("PRP$", Universal.PRONOUN)
    RB = PartOfSpeech("RB", Universal.ADVERB)
    RBR = PartOfSpeech("RBR", Universal.ADVERB)
    RBS = PartOfSpeech("RBS", Universal.ADVERB)
    RP = PartOfSpeech("RP", Universal.PARTICLE)
    SYM = PartOfSpeech("SYM", Universal.OTHER)
    TO = PartOfSpeech("TO", Universal.PARTICLE)
    UH = PartOfSpeech("UH", Universal.OTHER)
    WDT = PartOfSpeech("WDT", Universal.DETERMINER)
    WP = PartOfSpeech("WP", Universal.PRONOUN)
    WP_POS = PartOfSpeech("WP$", Universal.PRONOUN)
    WRB = PartOfSpeech("WRB", Universal.ADVERB)
    DOLLAR = PartOfSpeech("$", Universal.PUNCTUATION)
    LRB = PartOfSpeech("-LRB-", Universal.PUNCTUATION)
    RRB = PartOfSpeech("-RRB-", Universal.PUNCTUATION)
    LCB = PartOfSpeech("-LCB-", Universal.PUNCTUATION)
    RCB = PartOfSpeech("-RCB-", Universal.PUNCTUATION)
    RSB = PartOfSpeech("-RSB-", Universal.PUNCTUATION)
    LSB = PartOfSpeech("-LSB-", Universal.PUNCTUATION)
    COMMA = PartOfSpeech(",", Universal.PUNCTUATION)
    COLON = PartOfSpeech(":", Universal.PUNCTUATION)
    ADD = PartOfSpeech("ADD", Universal.OTHER)
    AFX = PartOfSpeech("AFX", Universal.ADPOSITION)
    NFP = PartOfSpeech("NFP", Universal.PUNCTUATION)
    PERIOD = PartOfSpeech(".", Universal.PUNCTUATION)
    POUND = PartOfSpeech("#", Universal.PUNCTUATION)
    HYPHEN = PartOfSpeech("-", Universal.PUNCTUATION)
    OPEN_QUOTE = PartOfSpeech("``", Universal.PUNCTUATION)
    CLOSE_QUOTE = PartOfSpeech("''", Universal.PUNCTUATION)
    QUOTE = PartOfSpeech('"', Universal.PUNCTUATION)
