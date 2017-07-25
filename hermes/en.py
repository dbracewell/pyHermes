import re
from hermes.language import ENGLISH
from hermes.core import Document
from spacy.en import English as enlp
from hermes.pos import PartOfSpeech

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

parser = enlp()


# class SentenceSegmenter(object):
#     def annotate(self, document: 'Document'):
#         index = 0
#         start = 0
#         for sen in split_multi(document.content):
#             start = document.content.index(sen, start)
#             document.create_annotation('sentence', start, start + len(sen), [("index", index)])
#             index += 1
#             start = start + len(sen)


class SpacyAnnotator(object):
    def __init__(self):
        self._regex = re.compile(r"(?:(?:\w+)|(?:\w+(\.\w+)+\.?))", re.UNICODE)

    def annotate(self, document: Document):
        parsed = parser(document.content)
        for token in parsed:
            t = document.create_annotation("token", token.idx, token.idx + len(token), [
                ("index", token.i),
                ("lemma", token.lemma_),
                ("prob", token.prob),
                ("pos", PartOfSpeech.of(token.tag_))
            ])
            if token.head is token:
                head_idx = None
            else:
                head_idx = token.head.i
            if head_idx:
                t.add_relation(target=head_idx, type="dep", relation=token.dep_)
        for entity in parsed.ents:
            document.create_annotation("entity", entity.start_char, entity.end_char, [("entity_type", entity.label_)])
        for i, sentence in enumerate(parsed.sents):
            document.create_annotation("sentence", sentence.start_char, sentence.end_char, [("index", i)])


tokenizer = SpacyAnnotator()
ENGLISH.set_annotator("token", tokenizer)
ENGLISH.set_annotator("entity", tokenizer)
ENGLISH.set_annotator("sentence", tokenizer)
