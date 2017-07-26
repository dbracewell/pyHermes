import sys

sys.path.append("/home/dbb/PycharmProjects/hermes-py/")
from hermes.core import *
from hermes.resource import Resource, resource
from hermes.io import json_reader


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
        return json_reader(self._source.reader(), one_per_line=True)


# timer = Timer(started=True)
# cnt = 0
# X = []
# Y = []
# for document in OnePerLine(JsonFormat()).read("/home/dbb/corpus/training_data/demographics/corpus.json"):
#     document.annotate("token")
#     cntr = Counter([x.lower() for x in document.tokens()])
#     X.append(dict(cntr.items()))
#     Y.append(document["AUTHOR_AGE"])
#     cnt += 1
#     if cnt % 100 == 0:
#         print("{} processed in {}".format(cnt, timer))
#
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction import DictVectorizer
# from sklearn.linear_model import SGDClassifier
#
# pipeline = Pipeline([
#     ("vect", DictVectorizer()),
#     ("clf", SGDClassifier(loss="log"))
# ])
#
# clf = pipeline.fit(X, Y)
#
# import pickle
#
# with open("model.p", "wb") as mdl:
#     pickle.dump(clf, mdl)
#
# test = Document("I love Dennys for their early bird special.")
# test.annotate("token")
# clf.predict(dict(Counter([x.lower() for x in test.tokens()]).items()))
from hermes.corpus import CorpusFormat
from hermes.corpus import Corpus

cnt = 0
corpus = Corpus.disk("json_opl", source="/home/dbb/corpus/training_data/demographics/corpus.json").cache()
for doc in corpus:
    doc.annotate("token")
    print(doc.annotation("entity"))
    cnt += 1
    exit(0)
