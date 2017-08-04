import sys

sys.path.append("/home/dbb/PycharmProjects/hermes-py/")
from hermes.core import *
from hermes.corpus import Corpus
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
import logging
from hermes.ml.features import BaseAnnotationExtractor, NormalizedValueCalculator
import numpy
import keras.preprocessing.text as tp
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.convolutional import Conv1D
from keras.layers.recurrent import LSTM

filename = '/home/dbb/wonderland.txt'
raw_text = open(filename).read().lower()
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))

n_chars = len(raw_text)
n_vocab = len(chars)
print("Total Characters: ", n_chars)
print("Total Vocab: ", n_vocab)
# prepare the dataset of input to output pairs encoded as integers
seq_length = 10
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
    seq_in = raw_text[i:i + seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)

# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)

# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.fit(X, y, epochs=5, batch_size=128)

int_to_char = dict((i, c) for i, c in enumerate(chars))
# pick a random seed
start = numpy.random.randint(0, len(dataX) - 1)
pattern = dataX[start]
print("Seed:")
# generate characters
for i in range(1000):
    x = numpy.reshape(pattern, (1, len(pattern), 1))
    x = x / float(n_vocab)
    prediction = model.predict(x, verbose=0)
    index = numpy.argmax(prediction)
    result = int_to_char[index]
    seq_in = [int_to_char[value] for value in pattern]
    sys.stdout.write(result)
    pattern.append(index)
    pattern = pattern[1:len(pattern)]
print("\nDone.")
exit(0)
logging.basicConfig(level=logging.INFO)

# # def get_tokens(hstr: HString):
# #     f = {}
# #     for t in hstr.tokens():
# #         if not t.is_stopword():
# #             f[t.lower()] = 1
# #     return f
# #
# #
# # from sklearn.pipeline import Pipeline
# # from sklearn.feature_extraction import DictVectorizer
# #
# # pp = Pipeline([
# #     ("hs", HStringFeaturizer(get_tokens)),
# #     ("dv", DictVectorizer())
# # ])
# #
# # fitted = pp.fit(Corpus.disk("json_opl", source="/home/dbb/annotated.json"))
#
# import nltk.corpus, nltk.tag, nltk.tag.api
# import nltk.chunk
# from nltk.metrics import edit_distance
# import enchant
#
# from nltk.chunk import ChunkParserI
# from nltk.chunk.util import tree2conlltags, conlltags2tree
# from nltk.tag import ClassifierBasedTagger
# from hermes.util import Timer
# import json
#
from hermes.util import Timer

timer = Timer(started=True)
# with open("/home/dbb/annotated.json", "w") as writer:
#     for document in Corpus.disk("json_opl", source="/home/dbb/corpus/training_data/demographics/corpus.json"):
#         document.annotate("token")
#         writer.write(document.to_json() + "\n")
# print(timer)
# exit(0)

#
# doc_list = []
# for dd in Corpus.disk("json_opl", "/home/dbb/annotated.json").generator():
#     doc_list.append(dd)
# print(len(doc_list))
# print(timer)
# exit(0)
#
#
# def chunk_trees2train_chunks(chunk_sents):
#     tag_sents = [tree2conlltags(sent) for sent in chunk_sents]
#     return [[((w, t), c) for (w, t, c) in sent] for sent in tag_sents]
#
#
# def prev_next_pos_iob(tokens, index, history):
#     word, pos = tokens[index]
#
#     if index == 0:
#         prevword, prevpos, previob = ('<START>',) * 3
#     else:
#         prevword, prevpos = tokens[index - 1]
#         previob = history[index - 1]
#
#     if index == len(tokens) - 1:
#         nextword, nextpos = ('<END>',) * 2
#     else:
#         nextword, nextpos = tokens[index + 1]
#
#     feats = {
#         'word': word,
#         'pos': pos,
#         'nextword': nextword,
#         'nextpos': nextpos,
#         'prevword': prevword,
#         'prevpos': prevpos,
#         'previob': previob
#     }
#     return feats
#
#
# class ClassifierChunker(ChunkParserI):
#     def __init__(self, train_sents, feature_detector=prev_next_pos_iob, **kwargs):
#         if not feature_detector:
#             feature_detector = self.feature_detector
#
#         train_chunks = chunk_trees2train_chunks(train_sents)
#         self.tagger = ClassifierBasedTagger(train=train_chunks,
#                                             feature_detector=feature_detector,
#                                             **kwargs)
#
#     def parse(self, tagged_sent):
#         if not tagged_sent: return None
#         chunks = self.tagger.tag(tagged_sent)
#         return conlltags2tree([(w, t, c) for ((w, t), c) in chunks])
#
#
# from nltk.corpus import conll2000
# from nltk.classify import MaxentClassifier
# from nltk.classify import SklearnClassifier
# from sklearn.linear_model.logistic import LogisticRegression
# from hermes.resource import resource
#
# import pycrfsuite as crf
#
# trainer = crf.Trainer(verbose=True)
#
# train_chunks = conll2000.chunked_sents('train.txt')
# for tree in train_chunks:
#     c = tree2conlltags(tree)
#     trainer.append([(x, y) for x, y, z in c],
#                    [z for x, y, z in c])
#
# trainer.set_params({
#     'c1': 1.0,
#     'c2': 1e-3,
#     'max_iterations': 100
# })
# # trainer.train('conll200.crfsuite')
#
# # classifier = SklearnClassifier(LogisticRegression())
# # test_chunks = conll2000.chunked_sents('test.txt')
# # builder = lambda toks: classifier.train(toks)
# # chunker = ClassifierChunker(train_chunks, classifier_builder=builder)
# # score = chunker.evaluate(test_chunks)
# # print(score)
# #
# # r = resource('chunker.pickle')
# # r.write_object(chunker)
# # print(score.accuracy())
# # chunker = r.read_object()
#
# from hermes.core import PartOfSpeech
#
# tagger = crf.Tagger()
# tagger.open('conll200.crfsuite')
#
# dd = Document("Calling to say that I care.")
# dd.annotate('token')
#
# lbls = tagger.tag([[t.content, t.pos().name] for t in dd.tokens()])
# print(lbls)
# # conll = tree2conlltags(chunker.parse([(t.content, t.pos().name) for t in dd.tokens()]))
# # current = None
# # ls = 0
# # le = 0
# # for (token, chunk) in zip(dd.tokens(), conll):
# #     tag = chunk[2]
# #     if tag.startswith('B-'):
# #         if current:
# #             dd.create_annotation('chunk', ls, le, [('pos', PartOfSpeech.of(current))])
# #         current = tag[2:]
# #         ls = token.start
# #         le = token.end
# #     elif tag.startswith('I-'):
# #         le = token.end
# #     else:
# #         if current:
# #             dd.create_annotation('chunk', ls, le, [('pos', PartOfSpeech.of(current))])
# #         current = None
# #         ls = 0
# #         le = 0
# #
# # if current:
# #     dd.create_annotation('chunk', ls, le, [('pos', PartOfSpeech.of(current))])
# #
# # for chunk in dd.annotation('chunk'):
# #     print(chunk, chunk.pos())
# exit(-1)
#
#
# class SpellingReplacer(object):
#     def __init__(self, dict_name='en', max_dist=2):
#         self.spell_dict = enchant.Dict(dict_name)
#         self.max_dist = max_dist
#
#     def replace(self, word):
#         if self.spell_dict.check(word):
#             return word
#         suggestions = self.spell_dict.suggest(word)
#
#         if suggestions and (0 if word[0] == suggestions[0][0] else 2) + \
#                 edit_distance(word, suggestions[0]) <= self.max_dist:
#             return suggestions[0]
#         else:
#             return word
#
#
# replacer = SpellingReplacer()
# print(replacer.replace('te'))
# print(replacer.replace('loove'))
#
# exit(-1)
#
#
# def conll_tag_chunks(chunk_sents):
#     tag_sents = [nltk.chunk.tree2conlltags(tree) for tree in chunk_sents]
#     return [[(t, c) for (w, t, c) in chunk_tags] for chunk_tags in tag_sents]
#
#
# def ubt_conll_chunk_accuracy(train_sents, test_sents):
#     train_chunks = conll_tag_chunks(train_sents)
#     test_chunks = conll_tag_chunks(test_sents)
#     u_chunker = nltk.tag.UnigramTagger(train_chunks)
#     ub_chunker = nltk.tag.BigramTagger(train_chunks, backoff=u_chunker)
#     # print('ub:', nltk.tag.accuracy(ub_chunker, test_chunks))
#     ubt_chunker = nltk.tag.TrigramTagger(train_chunks, backoff=ub_chunker)
#     # print('ubt:', nltk.tag.accuracy(ubt_chunker, test_chunks))
#     ut_chunker = nltk.tag.TrigramTagger(train_chunks, backoff=u_chunker)
#     # print('ut:', nltk.tag.accuracy(ut_chunker, test_chunks))
#     utb_chunker = nltk.tag.BigramTagger(train_chunks, backoff=ut_chunker)
#     # print('utb:', nltk.tag.accuracy(utb_chunker, test_chunks))
#
#
# # conll chunking accuracy test
# conll_train = nltk.corpus.conll2000.chunked_sents('train.txt')
# conll_test = nltk.corpus.conll2000.chunked_sents('test.txt')
# ubt_conll_chunk_accuracy(conll_train, conll_test)
#
# # treebank chunking accuracy test
# # treebank_sents = nltk.corpus.treebank_chunk.chunked_sents()
# # ubt_conll_chunk_accuracy(treebank_sents[:2000], treebank_sents[2000:])
#
# testD = Document("The man on the moon.")
# testD.annotate("token")
#
# exit(-1)
# # with open("/home/dbb/annotated.json", "w") as writer:
# #     for document in Corpus.disk("json_opl", source="/home/dbb/corpus/training_data/demographics/corpus.json"):
# #         document.annotate("token")
# #         writer.write(document.to_json() + "\n")
# #
# # exit(0)

from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

pipeline = Pipeline([
    ("dict", DictVectorizer()),
    ("clf", SGDClassifier(loss='modified_huber'))
])
extractor = BaseAnnotationExtractor(value_calculator=NormalizedValueCalculator(), lemmatize=False, lowercase=True)
X, Y = Corpus.disk("json_opl", source="/home/dbb/train.json").to_x_y(extractor, 'AUTHOR_AGE')
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2, random_state=42)
v = DictVectorizer(sparse=False)
o = LabelEncoder()
train_X = v.fit_transform(train_X)
train_Y = np_utils.to_categorical(o.fit_transform(train_Y), num_classes=4)

dim = len(v.vocabulary_)
nb_classes = len(train_Y[0])

model = Sequential()
# model.add(Dense(400, activation='relu', input_dim=dim))
model.add(Conv1D(50, input_shape=(None, 39243), kernel_size=128))
model.add(Dropout(0.5))
# model.add(Dense(200, activation='relu'))
# model.add(Dropout(0.5))
model.add(Dense(4, activation='linear'))
model.add(Activation('softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
test_X = v.transform(test_X)
test_Y = np_utils.to_categorical(o.transform(test_Y), num_classes=4)
model.fit(train_X, train_Y, epochs=5)
import numpy as np

pred_y = [o.inverse_transform(np.argmax(y)) for y in model.predict(test_X)]
test_Y = [o.inverse_transform(np.argmax(y)) for y in test_Y]


# exit(0)
# clf = pipeline.fit(train_X, train_Y)


def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """pretty print for confusion matrixes"""
    columnwidth = max([len(x) for x in labels] + [5])  # 5 is value length
    empty_cell = " " * columnwidth
    # Print header
    print("    " + empty_cell, end=" ")
    for label in labels:
        print("%{0}s".format(columnwidth) % label, end=" ")
    print()
    # Print rows
    for i, label1 in enumerate(labels):
        print("    %{0}s".format(columnwidth) % label1, end=" ")
        for j in range(len(labels)):
            cell = "%{0}.1f".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end=" ")
        print()


from sklearn.metrics import classification_report, confusion_matrix

# pred_Y = clf.predict(test_X)

print_cm(confusion_matrix(test_Y, pred_y, labels=o.classes_), labels=o.classes_)
print(classification_report(test_Y, pred_y, target_names=o.classes_))
#
# test_doc = Document("My kids loved the movie, but I thought it was hysterical.")
# test_doc.annotate("token")
# print(clf.predict([extractor.extract(test_doc)]))
#
# test_doc = Document("I bought it for my granddaughter and she just loved it!")
# test_doc.annotate("token")
# print(clf.predict([extractor.extract(test_doc)]))
