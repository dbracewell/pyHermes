import sys

from sklearn.feature_extraction.text import CountVectorizer

sys.path.append("/home/dbb/PycharmProjects/hermes-py/")
from hermes.util import Timer
from hermes.corpus import Corpus
from multiprocessing import Pool
from collections import Counter, defaultdict
from hermes.core import HString, Document
from hermes.util import compose
from itertools import filterfalse
import hermes.types as htypes
import pandas as pd
from bs4 import BeautifulSoup

train = pd.read_csv('/home/dbb/labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
train['cleaned'] = train.apply(lambda row: " ".join([x.lower() for x in BeautifulSoup(row[2], "lxml").get_text().split()]), axis=1)

cv = CountVectorizer(min_df=10)
X = cv.fit_transform(train.cleaned)
Y = train.sentiment
print(X.shape)
print(Y.shape)


# def process_doc(doc):
#     return set(filter(lambda pc: len(pc) >= 3,
#                       map(compose(HString.lemma, HString.strip),
#                           filterfalse(HString.is_stopword, doc.annotation(htypes.PHRASE_CHUNK)))))
#
#
# cntr = defaultdict(int)
# timer = Timer(started=True)
# # for chunks in map(process_doc, Corpus.disk(fmt='json_opl', source='/home/dbb/annotated2.json_opl')):
# #     cntr.update(chunks)
# for doc in Corpus.disk(fmt='json_opl', source='/home/dbb/annotated2.json_opl'):
#     pass
#     # for tokn in set(filter(lambda pc: len(pc) >= 3,
#     #                        map(compose(HString.lemma, HString.strip),
#     #                            filterfalse(HString.is_stopword, doc.annotation(htypes.PHRASE_CHUNK))))):
#     #     pass
#
# print(timer)
