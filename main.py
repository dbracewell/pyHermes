import sys

sys.path.append("/home/dbb/PycharmProjects/hermes-py/")
from hermes.core import *
from hermes.resource import Resource, resource
from hermes.io import plain_text_reader

doc = Document("A plane crashed near Yonkers, but John Snow was not there.")


# doc.annotate("token")
# for sentence in doc.annotation('sentence'):
#     print(sentence)
#     print([(t["lemma"], t.head()) for t in sentence.tokens()])
#     print([(t, t["entity_type"]) for t in sentence.annotation('entity')])


class Corpus(object):
    def generator(self):
        pass


class FileCorpus(Corpus):
    def __init__(self, source: [Resource, str]):
        self._source = resource(source)

    def annotate(self, *args):
        for document in self.generator():
            document.annotate(*args)
            yield document

    def generator(self):
        return plain_text_reader(self._source.reader(), one_per_line=True)


corpus = FileCorpus("/home/dbb/test/docs.txt")
for document in corpus.annotate("token"):
    print(">>>", document.tokens(), "<<<")
