import zipfile

import requests
import shutil
from clint.textui import progress
from os.path import isdir, join, expanduser

from os import mkdir, remove, listdir

data_folder = join(expanduser('~'), "languageflow_data")


def init_folder(folder):
    is_folder = isdir(folder)
    if not is_folder:
        try:
            shutil.rmtree(folder)
        except Exception as e:
            pass
        mkdir(folder)
        return False
    return True


def reset_folder(folder):
    if isdir(folder):
        shutil.rmtree(folder)
    mkdir(folder)


def post_process(component):
    if component == "son_word2vec_news_vn":
        from languageflow.download import son_word2vec_news_vn
        son_word2vec_news_vn.post_process()
    if component == "hoang_word2vec_news_vn":
        from languageflow.download import hoang_word2vec_news_vn
        hoang_word2vec_news_vn.post_process()


def download_component(component, force=False):
    init_folder(data_folder)
    component_folder = join(data_folder, component)
    if isdir(component_folder) and not force:
        print("[Warning] Component '{}' is existed".format(component))
        print("Use -f option to force download")
        return
    reset_folder(component_folder)
    url = "https://github.com/undertheseanlp/data/archive/{}.zip".format(
        component)
    r = requests.get(url, stream=True)
    path = join(data_folder, 'temp.zip')
    try:
        remove(path)
    except:
        pass
    with open(path, 'wb') as f:
        fail_time = 0
        while fail_time < 3:
            try:
                total_length = int(r.headers.get('content-length'))
                for chunk in progress.bar(r.iter_content(chunk_size=1024),
                                          expected_size=(
                                              total_length / 1024) + 1):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                break
            except Exception as e:
                fail_time += 1
    zipfile.ZipFile(path, 'r').extractall(component_folder)
    remove(path)
    file = listdir(component_folder)[0]
    for f in listdir(join(component_folder, file)):
        shutil.move(join(component_folder, file, f), join(component_folder, f))
    shutil.rmtree(join(component_folder, file))
    print("Component '{}' is downloaded successfully.".format(component))
    post_process(component)


if __name__ == '__main__':
    # component = "hoang_word2vec_news_vn"
    # post_process(component)
    pass

