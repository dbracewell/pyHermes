import csv
import regex as re
import gensim
import pandas as pd

hashtag_pattern = re.compile('#[^\s\p{P}]+')
dictionary = gensim.corpora.Dictionary()

texts = []
with open('/home/dbb/PycharmProjects/twitter_crawler/music.csv') as rdr:
    csv = csv.reader(rdr)
    for row in csv:
        if len(row) > 0:
            text = row[0]
            tags = [t.lower() for t in hashtag_pattern.findall(text)]
            if len(tags) > 0:
                texts.append(dictionary.doc2bow(tags, allow_update=True))


lda_model = gensim.models.LdaModel(corpus=texts, id2word=dictionary, alpha='auto', num_topics=50, iterations=500)
for i in range(lda_model.num_topics):
    print([x[0] for x in lda_model.show_topic(i)])

def topic_prob_extractor(gensim_hdp):
    shown_topics = gensim_hdp.show_topics(num_topics=-1, formatted=False)
    topics_nos = [x[0] for x in shown_topics]
    weights = [sum([item[1] for item in shown_topics[topicN][1]]) for topicN in topics_nos]

    return pd.DataFrame({'topic_id': topics_nos, 'weight': weights})


lda_model = gensim.models.HdpModel(corpus=texts, id2word=dictionary, T=20)
df = topic_prob_extractor(lda_model)
for row in df.iterrows():
    print(row[1]['topic_id'], row[1]['weight'])

# for topic in lda_model.show_topics(num_topics=-1, num_words=10):
#     id = topic[0]
#     words = topic[1]
#     wout = []
#     for w in words.split(' '):
#         if '*' in w:
#             wout.append(w.split('*')[1])
#     print(id, wout)
