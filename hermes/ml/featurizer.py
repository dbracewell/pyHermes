from sklearn.feature_extraction.text import TransformerMixin


class Extractor:
    def extract(self, hstr):
        raise NotImplementedError

    @staticmethod
    def chain(*args):
        return ChainExtractor(*args)


class ChainExtractor(Extractor):
    def __init__(self, *extractors):
        self._extractors = extractors

    def extract(self, hstr):
        d = dict()
        for ex in self._extractors:
            d.update(ex.extract(hstr))
        return d


class HStringFeaturizer(TransformerMixin):
    def __init__(self, *featurizers):
        self._featurizers = featurizers

    def fit(self, texts, y=None):
        return self

    def transform(self, X):
        X_trans = []
        for x in X:
            features = {}
            for func in self._featurizers:
                features.update(func(x))
            X_trans.append(features)
        return X_trans
