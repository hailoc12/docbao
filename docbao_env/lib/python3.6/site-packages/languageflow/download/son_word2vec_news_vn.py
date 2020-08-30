from os.path import join, expanduser
from os import listdir, remove

import shutil

data_folder = join(expanduser('~'), "languageflow_data")
component = "son_word2vec_news_vn"


def concat_files(dest_file, source_files):
    with open(dest_file, 'wb') as wfd:
        for f in source_files:
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd, 1024 * 1024 * 10)


def post_process():
    component_folder = join(data_folder, component)
    files = listdir(component_folder)
    files = sorted([f for f in files if f not in [".gitignore", "README.md"]])
    file = files[0][:-3]
    concat_files(join(component_folder, file),
                 [join(component_folder, f) for f in files])
    for f in files:
        remove(join(component_folder, f))
