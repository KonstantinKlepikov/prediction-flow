"""
CatagoryEncoder to convert term to number.
"""

# Authors: Hongwei Zhang
# License: MIT


import numpy as np
from collections import Counter

from .base import CategoryColumn


class CategoryEncoder(CategoryColumn):
    """Encoder for category type feature.

    Parameters
    ----------
    min_cnt : int, default=5
        Minimum count of term.

    Attributes
    ----------
    min_cnt : int, default=5
        Minimum count of term.

    word2idx : dict
        Mappings from term to index.

    idx2word : dict
        Mappings from index to term.
    """
    def __init__(self, min_cnt=5):
        self.min_cnt = min_cnt
        self.word2idx = dict()
        self.idx2word = dict()

    def fit(self, x, y=None):
        """Fit this transformer.

        Parameters
        ----------
        x : array-like
            One column of training data.
        y : array-like, default=None, ignored
            Training targets.

        Returns
        -------
        self : CategoryEncoder
            This CategoryEncoder.
        """
        counter = Counter(np.asarray(x).ravel())

        selected_terms = sorted(
            list(filter(lambda x: counter[x] >= self.min_cnt, counter)))

        self.word2idx = dict(
            zip(selected_terms, range(0, len(selected_terms))))

        if '__UNKNOWN__' not in self.word2idx:
            self.word2idx['__UNKNOWN__'] = len(self.word2idx)

        self.idx2word = {index: word for word, index in self.word2idx.items()}

        return self

    def transform(self, x):
        """Transform x by this fitted transformer.

        Parameters
        ----------
        x : array-like
            Column data to be transformed.

        Returns
        -------
        transformed_x : array-like
            Transformed data.
        """
        transformed_x = list()
        for term in np.asarray(x).ravel():
            try:
                transformed_x.append(self.word2idx[term])
            except KeyError:
                transformed_x.append(self.word2idx['__UNKNOWN__'])

        return np.asarray(transformed_x, dtype=np.int)

    def dimension(self):
        return len(self.word2idx)