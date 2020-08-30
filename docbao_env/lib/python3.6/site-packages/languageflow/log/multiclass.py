import json
from os.path import join
from languageflow.util.file_io import write
from sklearn import metrics
from sklearn.preprocessing import LabelBinarizer


class MulticlassLogger:
    """
    Analyze and save multiclass results
    """

    @staticmethod
    def log(X_test, y_test, y_pred, folder):
        """

        Parameters
        ----------
        X_test : list of string
            Raw texts
        y_test : list of string
            Test labels
        y_pred : list of string
            Predict labels
        folder : string
            log folder
        """
        labels = set(y_test + y_pred)
        score = {}
        for label in labels:
            score[label] = {}
            TP, FP, TN, FN = (0, 0, 0, 0)

            for i, label_test in enumerate(y_test):
                label_pred = y_pred[i]
                if label == label_test:
                    if label == label_pred:
                        TP += 1
                    else:
                        FN += 1
                else:
                    if label == label_pred:
                        FP += 1
                    else:
                        TN += 1
            score[label] = {
                "TP": TP,
                "FP": FP,
                "TN": TN,
                "FN": FN,
                "accuracy": accuracy_score(TP, FP, TN, FN),
                "precision": precision_score(TP, FP, TN, FN),
                "recall": recall_score(TP, FP, TN, FN),
                "f1": f1_score(TP, FP, TN, FN),
            }

        # generate result
        result = {
            "X_test": X_test,
            "y_test": y_test,
            "y_pred": y_pred,
            "score": score,
            "type": "multiclass"
        }

        content = json.dumps(result, ensure_ascii=False)
        log_file = join(folder, "result.json")
        write(log_file, content)
        print("Result is written in {}".format(log_file))

        binarizer = LabelBinarizer()
        y_test = binarizer.fit_transform(y_test)
        y_pred = binarizer.transform(y_pred)
        print("F1 Weighted:",
              metrics.f1_score(y_test, y_pred, average='weighted'))


def accuracy_score(TP, FP, TN, FN):
    return round((TP + TN) / (TP + FP + TN + FN), 2)


def precision_score(TP, FP, TN, FN):
    try:
        return round(TP / (TP + FP), 2)
    except:
        return 0


def recall_score(TP, FP, TN, FN):
    try:
        return round(TP / (TP + FN), 2)
    except:
        return 0


def f1_score(TP, FP, TN, FN):
    p = precision_score(TP, FP, TN, FN)
    r = recall_score(TP, FP, TN, FN)
    try:
        f1 = round((2 * p * r) / (p + r), 2)
    except:
        f1 = 0
    return f1
