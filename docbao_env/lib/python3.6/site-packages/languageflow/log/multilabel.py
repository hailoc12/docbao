import sklearn
from sklearn.preprocessing import MultiLabelBinarizer
import json
from os.path import join
from languageflow.util.file_io import write


class MultilabelLogger:
    """
    Analyze and save multilabel results to
    multilabel.json and result.json files
    """

    @staticmethod
    def log(X_test, y_test, y_pred, log_folder):
        """

        Parameters
        ----------
        X_test : list of string
            Raw texts
        y_test : list of string
            Test labels
        y_pred : list of string
            Predict labels
        log_folder : string
            path to log folder
        """

        labels = set(sum(y_test + y_pred, ()))
        score = {}
        for label in labels:
            score[label] = {}
            TP, FP, TN, FN = (0, 0, 0, 0)

            for i in range(len(y_test)):
                if label in y_test[i]:
                    if label in y_pred[i]:
                        TP += 1
                    else:
                        FN += 1
                else:
                    if label in y_pred[i]:
                        FP += 1
                    else:
                        TN += 1
            score[label] = {
                "TP": TP,
                "FP": FP,
                "TN": TN,
                "FN": FN,
                "accuracy": _accuracy_score(TP, FP, TN, FN),
                "precision": _precision_score(TP, FP, TN, FN),
                "recall": _recall_score(TP, FP, TN, FN),
                "f1": _f1_score(TP, FP, TN, FN),
            }
        result = {
            "X_test": X_test,
            "y_test": y_test,
            "y_pred": y_pred,
            "score": score,
            "type": "multilabel"
        }
        content = json.dumps(result, ensure_ascii=False)
        log_file = join(log_folder, "multilabel.json")
        write(log_file, content)
        print("Multilabel analyze report is saved in log folder")

        binarizer = MultiLabelBinarizer()
        y = [{i for sub in y_test for i in sub}.union(
            {i for sub in y_pred for i in sub})]
        binarizer.fit_transform(y)
        y_test = binarizer.transform(y_test)
        y_pred = binarizer.transform(y_pred)

        from sklearn.metrics import accuracy_score, f1_score
        result = {
            "Sample": len(X_test),
            "Accuracy": accuracy_score(y_test, y_pred),
            "F1 Micro": f1_score(y_test, y_pred, average='micro'),
            "F1 Macro": f1_score(y_test, y_pred, average='macro'),
            "F1 Weighted": f1_score(y_test, y_pred, average='weighted'),
        }
        content = json.dumps(result, ensure_ascii=False)
        log_file = join(log_folder, "result.json")
        write(log_file, content)
        print("Result is saved in log folder")
        print("Classification Report")
        print(json.dumps(result, indent=4, sort_keys=True))


def _accuracy_score(TP, FP, TN, FN):
    return round((TP + TN) / (TP + FP + TN + FN), 2)


def _precision_score(TP, FP, TN, FN):
    try:
        return round(TP / (TP + FP), 2)
    except:
        return 0


def _recall_score(TP, FP, TN, FN):
    try:
        return round(TP / (TP + FN), 2)
    except:
        return 0


def _f1_score(TP, FP, TN, FN):
    p = _precision_score(TP, FP, TN, FN)
    r = _recall_score(TP, FP, TN, FN)
    try:
        f1 = round((2 * p * r) / (p + r), 2)
    except:
        f1 = 0
    return f1
