import joblib
import numpy
from os.path import join
from sklearn.preprocessing import MultiLabelBinarizer

from languageflow.experiment import Experiment
from languageflow.transformer.count import CountVectorizer
from languageflow.transformer.tfidf import TfidfVectorizer

from languageflow.validation.validation import TrainTestSplitValidation
from languageflow.transformer.number import NumberRemover

class Flow:
    """
    Pipeline to build a model

    Examples
    --------

    >>> from languageflow.flow import Flow
    >>> flow = Flow()
    >>> flow.data(X, y)
    >>> flow.transform(TfidfTransformer())
    >>> model = Model(SGD(), "SGD")
    >>> flow.add_model(model)
    >>> flow.train()
    """
    def __init__(self):
        self.models = []
        self.lc_range = [1]
        self.result = []
        self.validation_method = TrainTestSplitValidation()
        self.scores = set()
        self.log_folder = "."
        self.export_folder = "."
        self.transformers = []

    def data(self, X=None, y=None, sentences=None):
        """
        Add data to flow

        """
        self.X = X
        self.y = y
        self.sentences = sentences

    def transform(self, transformer):
        """
        Add transformer to flow and apply transformer to data in flow

        Parameters
        ----------
        transformer : Transformer
            a transformer to transform data
        """
        self.transformers.append(transformer)
        from languageflow.transformer.tagged import TaggedTransformer

        if isinstance(transformer, TaggedTransformer):
            self.X, self.y = transformer.transform(self.sentences)
        if isinstance(transformer, TfidfVectorizer):
            self.X = transformer.fit_transform(self.X)
        if isinstance(transformer, CountVectorizer):
            self.X = transformer.fit_transform(self.X)
        if isinstance(transformer, NumberRemover):
            self.X = transformer.transform(self.X)

        if isinstance(transformer, MultiLabelBinarizer):
            self.y = transformer.fit_transform(self.y)

    def add_model(self, model):
        """
        Add model to flow
        """
        self.models.append(model)

    def add_score(self, score):
        self.scores.add(score)

    def set_learning_curve(self, start, stop, offset):
        self.lc_range = numpy.arange(start, stop, offset)

    def set_validation(self, validation):
        self.validation_method = validation

    def train(self):
        """
        Train model with transformed data
        """
        for i, model in enumerate(self.models):
            N = [int(i * len(self.y)) for i in self.lc_range]
            for n in N:
                X = self.X[:n]
                y = self.y[:n]
                e = Experiment(X, y, model.estimator, self.scores,
                               self.validation_method)
                e.log_folder = self.log_folder
                e.train()

    def export(self, model_name, export_folder):
        """
        Export model and transformers to export_folder

        Parameters
        ----------
        model_name: string
            name of model to export
        export_folder: string
            folder to store exported model and transformers
        """
        for transformer in self.transformers:
            if isinstance(transformer, MultiLabelBinarizer):
                joblib.dump(transformer,
                            join(export_folder, "label.transformer.bin"),
                            protocol=2)
            if isinstance(transformer, TfidfVectorizer):
                joblib.dump(transformer,
                            join(export_folder, "tfidf.transformer.bin"),
                            protocol=2)
            if isinstance(transformer, CountVectorizer):
                joblib.dump(transformer,
                            join(export_folder, "count.transformer.bin"),
                            protocol=2)
            if isinstance(transformer, NumberRemover):
                joblib.dump(transformer,
                            join(export_folder, "number.transformer.bin"),
                            protocol=2)
        model = [model for model in self.models if model.name == model_name][0]
        e = Experiment(self.X, self.y, model.estimator, None)
        model_filename = join(export_folder, "model.bin")
        e.export(model_filename)
