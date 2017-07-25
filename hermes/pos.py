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
_lookup = {}


class PartOfSpeech:
    def __init__(self, tag: str, coarse=None):
        tag = tag.upper()
        if tag in _lookup:
            raise Exception("{0} is already defined".format(tag))
        _lookup[tag] = self
        self._tag = tag
        if coarse:
            self._coarse = coarse
        else:
            self._coarse = self

    def is_noun(self):
        return self.coarse.name == NOUN.coarse

    def is_verb(self):
        return self.coarse.name == VERB.coarse

    def is_punctuation(self):
        return self.coarse.name == PUNCTUATION.coarse

    @staticmethod
    def guess(hs):
        g = UNKNOWN
        for token in hs.tokens():
            g = token.pos()
        return g

    @staticmethod
    def of(tag):
        tag = tag.upper()
        if tag in _lookup:
            return _lookup[tag]
        return UNKNOWN

    def __repr__(self) -> str:
        return self._tag

    def __eq__(self, other):
        if isinstance(other, PartOfSpeech):
            return self._tag == other._tag
        return False

    @property
    def name(self):
        return self._tag

    @property
    def coarse(self):
        return self._coarse

    def __str__(self):
        return self._tag


UNKNOWN = PartOfSpeech("ANY")

NOUN = PartOfSpeech("NOUN")
NN = PartOfSpeech("NN", NOUN)
NNP = PartOfSpeech("NNP", NOUN)
NNS = PartOfSpeech("NNS", NOUN)
NNPS = PartOfSpeech("NNPS", NOUN)

VERB = PartOfSpeech("VERB")
VB = PartOfSpeech("VB", VERB)
VBD = PartOfSpeech("VBD", VERB)
VBG = PartOfSpeech("VBG", VERB)
VBN = PartOfSpeech("VBN", VERB)
VBP = PartOfSpeech("VBP", VERB)
VBZ = PartOfSpeech("VBZ", VERB)

PUNCTUATION = PartOfSpeech("PUNCTUATION")
PERIOD = PartOfSpeech(".", PUNCTUATION)
POUND = PartOfSpeech("#", PUNCTUATION)
HYPHEN = PartOfSpeech("-", PUNCTUATION)
OPEN_QUOTE = PartOfSpeech("``", PUNCTUATION)
CLOSE_QUOTE = PartOfSpeech("''", PUNCTUATION)
QUOTE = PartOfSpeech('"', PUNCTUATION)
