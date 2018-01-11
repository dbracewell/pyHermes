import spacy
from hermes.util import Timer
from hermes.core import Document
from hermes.corpus import Corpus
nlp = spacy.load('en')

timer = Timer(started=True)
tokcount = 0
doccount = 0
for doc in Corpus.disk('txt_opl',source='/home/dbb/corpus/gen.txt'):
    print(doc)
    doc.annotate('token')
    tokcount += len(doc)
    doccount += 1
timer.stop()
print(timer.elapsed_seconds(),
      tokcount,
      (tokcount / timer.elapsed_seconds()),
      doccount,
      (doccount / timer.elapsed_seconds()))


# with open('/home/dbb/corpus/gen.txt') as fp:
#     timer = Timer(started=True)
#     tokcount = 0
#     doccount = 0
#     for doc in nlp.pipe(fp):
#         # Document.from_spacy(parsed=doc)
#         tokcount += len(doc)
#         doccount += 1
#     timer.stop()
#     print(timer.elapsed_seconds(),
#           tokcount,
#           (tokcount / timer.elapsed_seconds()),
#           doccount,
#           (doccount / timer.elapsed_seconds()))
