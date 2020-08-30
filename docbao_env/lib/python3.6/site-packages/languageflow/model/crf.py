import pycrfsuite


class CRF:
    def __init__(self, params={'c1':0.1, 'c2':0.01, 'feature.minfreq':0}, filename=None):
        self.estimator = None
        self.params = params
        self.filename = filename

    def fit(self, X, y):
        """Fit CRF according to X, y

        Parameters
        ----------
        X : list of text
            each item is a text
        y: list
           each item is either a label (in multi class problem) or list of
           labels (in multi label problem)
        """
        trainer = pycrfsuite.Trainer(verbose=True)
        for xseq, yseq in zip(X, y):
            trainer.append(xseq, yseq)

        trainer.set_params(self.params)
        if self.filename:
            filename = self.filename
        else:
            filename = 'model.tmp'
        trainer.train(filename)
        tagger = pycrfsuite.Tagger()
        tagger.open(filename)
        self.estimator = tagger

    def predict(self, X):
        """Predict class labels for samples in X.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            Samples.
        """
        if isinstance(X[0], list):
            return [self.estimator.tag(x) for x in X]
        return self.estimator.tag(X)
