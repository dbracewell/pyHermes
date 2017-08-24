import sys

from keras.layers import Dense, Activation, Dropout
from keras.models import Sequential
from keras.utils import np_utils
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder

sys.path.append("/home/dbb/PycharmProjects/hermes-py/")
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from hermes.corpus import Corpus
from hermes.ml.evaluation import evaluate_model
import gensim
from hermes.ml.features import Extractor, NormalizedValueCalculator, BaseAnnotationExtractor, BinaryValueCalculator
from keras.optimizers import SGD
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# logging.basicConfig(level=logging.INFO)

# texts = []
# dictionary = gensim.corpora.Dictionary()
# for doc in Corpus.disk(fmt='json_opl', source='/home/dbb/annotated.json'):
#     texts.append(dictionary.doc2bow([t.lemma() for t in doc.tokens() if not t.is_stopword()], allow_update=True))
# lda_model = gensim.models.LdaModel(corpus=texts, id2word=dictionary, alpha='auto')
# lda_model.save('lda.model')
#
# lda_model = gensim.models.LdaModel.load('lda.model')
pipeline = Pipeline([
    # ("dict", DictVectorizer()),
    ("clf", RandomForestClassifier(n_estimators=100))
])

extractor = BaseAnnotationExtractor(value_calculator=BinaryValueCalculator(), lemmatize=False, lowercase=True)
X, Y = Corpus.disk("json_opl", source="/home/dbb/annotated2.json_opl").to_x_y(extractor, 'AUTHOR_AGE')

# class ldaExtractor(Extractor):
#     def extract(self, hstr):
#         lemmas = [t.lemma() for t in hstr.tokens() if not t.is_stopword()]
#         bow = lda_model.id2word.doc2bow(lemmas)
#         vec = np.zeros(100)
#         for topic, score in lda_model[bow]:
#             vec[topic] = score
#         return vec


# X, Y = Corpus.disk("json_opl", source="/home/dbb/annotated.json").to_x_y(ldaExtractor(), 'AUTHOR_AGE')
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2, random_state=42)
# clf = pipeline.fit(train_X, train_Y)
# pred_y = clf.predict(test_X)


#
# test_doc = Document("My kids loved the movie, but I thought it was hysterical.")
# test_doc.annotate("token")
# print(clf.predict([extractor.extract(test_doc)]))
#
# test_doc = Document("I bought it for my granddaughter and she just loved it!")
# test_doc.annotate("token")
# print(clf.predict([extractor.extract(test_doc)]))

v = DictVectorizer(sparse=False)
o = LabelEncoder()
# train_X = v.fit_transform(train_X)

train_X = v.fit_transform(train_X)
train_Y = np_utils.to_categorical(o.fit_transform(train_Y), num_classes=4)
nb_classes = len(train_Y[0])

model = Sequential()
model.add(Dense(300, activation='sigmoid', input_shape=(len(v.vocabulary_),)))
model.add(Dropout(0.2))
model.add(Dense(4, activation='linear'))
model.add(Activation('softmax'))
model.compile(optimizer="sgd", loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(train_X, train_Y, epochs=20)

test_X = v.transform(test_X)
test_Y = np_utils.to_categorical(o.transform(test_Y), num_classes=4)

pred_y = [o.inverse_transform(np.argmax(y)) for y in model.predict(test_X)]
test_Y = [o.inverse_transform(np.argmax(y)) for y in test_Y]

evaluate_model(test_Y, pred_y, o.classes_)
