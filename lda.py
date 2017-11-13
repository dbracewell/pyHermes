import gensim
import csv
from hermes.core import Document

texts = []
tokens = []
dictionary = gensim.corpora.Dictionary()
with open('/home/dbb/analysis/kombucha/refreshment.csv') as rdr:
    csv = csv.reader(rdr)
    for row in csv:
        if len(row) > 0:
            doc = Document(row[0])
            doc.annotate('token')
            tokens.append([t.lower() for t in doc.tokens() if not t.is_stopword() and (t.pos().is_noun())])
            dictionary.doc2bow(tokens[-1], allow_update=True)

dictionary.filter_n_most_frequent(10)
for text in tokens:
    texts.append(dictionary.doc2bow(text))

lda_model = gensim.models.LdaModel(corpus=texts, id2word=dictionary, alpha='auto', num_topics=10, iterations=500)
# HdpModel(corpus=texts, id2word=dictionary)
# .LdaModel(corpus=texts, id2word=dictionary, alpha='auto', num_topics=20, iterations=500)

# for topic in lda_model.show_topics(num_topics=-1, num_words=10):
#     id = topic[0]
#     words = topic[1]
#     wout = []
#     for w in words.split(' '):
#         if '*' in w:
#             wout.append(w.split('*')[1])
#     print(id, wout)

for i in range(lda_model.num_topics):
    print([x[0] for x in lda_model.show_topic(i)])
