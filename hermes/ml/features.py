from .featurizer import Extractor
import typing
from collections import Counter


class ValueCalculator:
    def calculate(self, feature_dict: [typing.Dict[str, float], Counter]) -> typing.Dict[str, float]:
        raise NotImplementedError


class BinaryValueCalculator(ValueCalculator):
    def calculate(self, feature_dict):
        return dict([(k, 1.0) for k, v in feature_dict.items()])


class RawValueCalculator(ValueCalculator):
    def calculate(self, feature_dict):
        return dict(feature_dict)


class NormalizedValueCalculator(ValueCalculator):
    def calculate(self, feature_dict):
        dict_sum = sum(feature_dict.values())
        return dict([(k, v / dict_sum) for k, v in feature_dict.items()])


class BaseAnnotationExtractor(Extractor):
    def __init__(self, annotation_type="token", value_calculator=RawValueCalculator, ignore_stopwords=True,
                 lemmatize=False, lowercase=False):
        self._ignore_stopwords = ignore_stopwords
        self._value_calculator = value_calculator
        self._lowercase = lowercase
        self._lemmatize = lemmatize
        self._annotation_type = annotation_type

    def extract(self, hstr):
        cntr = Counter(self.__to_string(hstr.annotation(self._annotation_type)))
        return self._value_calculator.calculate(feature_dict=cntr)

    def __to_string(self, annotation_list):
        to_return = []
        for annotation in annotation_list:
            content = annotation.lemma() if self._lemmatize else annotation.content
            # print(content, self._ignore_stopwords, annotation.is_stopword())
            if self._ignore_stopwords and annotation.is_stopword():
                continue
            if self._lowercase:
                content = content.lower()
            to_return.append(content)
        return to_return
