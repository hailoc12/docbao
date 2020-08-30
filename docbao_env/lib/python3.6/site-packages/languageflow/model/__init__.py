class Model:
    def __init__(self, estimator, name):
        self.estimator = estimator
        self.name = name

    def fit(self, X, y, filename=None):
        pass

    def predict(self, X):
        pass


class BaseModel:
    def __init__(self, transformer):
        self.transformer = transformer

    def load_data(self):
        raise Exception("Need implement")

    def fit_transform(self):
        raise Exception("Need implement")

    def train(self):
        raise Exception("Need implement")

    def export(self):
        raise Exception("Need implement")
