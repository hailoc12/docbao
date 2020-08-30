import json
import time
import io
from os import mkdir
from os.path import join
from datetime import datetime
from pprint import pprint


class ModelProfiling:
    def __init__(self):
        self.data = {}

    def start_train(self):
        self.start = time.time()

    def end_train(self):
        self.end = time.time()
        self.duration = self.end - self.start

    def save(self, filename="model.profile", folder=".profile", prefix=True):
        try:
            mkdir(folder)
        except:
            pass
        self.data["duration"] = self.duration
        filename = join(folder, filename)
        if prefix:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename += "_" + timestamp
        with io.open(filename, "w", encoding="utf8") as f:
            content = json.dumps(self.data, indent=4, sort_keys=True, ensure_ascii=False)
            f.write(content.decode("utf-8"))

    def add(self, key, value):
        self.data[key] = value

    def show(self):
        pprint(self.data, indent=2)
