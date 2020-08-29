import fasttext


def load(model_type, bin_path):
    if model_type == "FastText":
        from languageflow.model.fasttext import FastTextClassifier
        estimator = fasttext.load_model(bin_path)
        model = FastTextClassifier()
        model.estimator = estimator
        return model
