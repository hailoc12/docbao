from __future__ import absolute_import
import os

from languageflow.transformer.text import Text

import fasttext as ft
from languageflow.util.file_io import write


class FastTextClassifier:
    """ Only support multiclass classification
    """
    def __init__(self):
        self.estimator = None
        self.prefix = "__label__"

    def fit(self, X, y, model_filename=None):
        """Fit FastText according to X, y

        Parameters
        ----------
        X : list of string
            each item is a raw text
        y : list of string
            each item is a label
        """
        train_file = "temp.train"
        X = [x.replace("\n", " ") for x in X]
        y = [_.replace(" ", "-") for _ in y]
        lines = ["{}{} , {}".format(self.prefix, j, i) for i, j in zip(X, y)]
        content = "\n".join(lines)
        write(train_file, Text(content))
        if model_filename:
            self.estimator = ft.supervised(train_file, model_filename)
        else:
            self.estimator = ft.supervised(train_file, 'model.tmp')
            os.remove('model.tmp.bin')
        os.remove(train_file)

    def _remove_prefix(self, label):
        if self.prefix in label:
            label = label[len(self.prefix):]
        return label

    def predict(self, X):
        """ In order to obtain the most likely label for a list of text

        Parameters
        ----------
        X : list of string
            Raw texts

        Returns
        -------
        C : list of string
            List labels
        """
        x = X
        if not isinstance(X, list):
            x = [X]
        y = self.estimator.predict(x)
        y = [item[0] for item in y]
        y = [self._remove_prefix(label) for label in y]
        if not isinstance(X, list):
            y = y[0]
        return y
