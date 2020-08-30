class Validation:
    def __init__(self):
        pass


class TrainTestSplitValidation(Validation):
    def __init__(self, test_size=0.2):
        self.test_size = test_size


class CrossValidation(Validation):
    def __init__(self, cv):
        self.cv = cv
