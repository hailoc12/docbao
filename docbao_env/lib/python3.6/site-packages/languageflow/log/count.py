import json
from os.path import join
import joblib
from languageflow.util.file_io import write


class CountLogger:
    """
    Analyze and save tfidf results
    """

    @staticmethod
    def log(model_folder, binary_file="count.transformer.bin",
            log_folder="analyze"):
        """
        Parameters
        ----------
        model_folder : string
            folder contains binaries file of model
        binary_file : string
            file path to count transformer binary file
        log_folder : string
            log folder
        """
        file = join(model_folder, binary_file)
        vectorizer = joblib.load(file)
        output = []

        for token in vectorizer.vocabulary_:
            index = vectorizer.vocabulary_[token]
            ngram = len(token.split(" "))
            output.append({
                "token": token,
                "ngram": ngram,
                "period": vectorizer.period_[index].item(),
                "df": vectorizer.df_[index],
            })
        output = sorted(output, key=lambda item: item["df"])
        content = json.dumps(output, ensure_ascii=False)
        write(join(log_folder, "count.json"), content)
