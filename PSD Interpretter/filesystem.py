import os, zipfile, shutil, json

from Page.bcs_tokenizer import Page

import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def folder_list(path):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for files in (filenames):
            f.append(f"{dirpath}/{files}")
        break
    f.sort(key=natural_keys)
    return f

def folder_list_ext_spec(path, ext = ".bcs"):
    f = []
    for file in folder_list(path):
        if file.endswith(ext):
            f.append(file)
    print(f)
    return f

class bcz:
    def __init__(self):
        with zipfile.ZipFile('spam.zip', 'w') as myzip:
            myzip.comment = "bu bir test dosyasıdır ve çıkışa yakın düzeltilmelidir".encode()
            myzip.write('export.bcs')
            myzip.close()

class Episode_Metadata:

    # Episode details
    name = ""     # Episode name
    volume = 0    # Volume that contain this episode
    episode = 0   # Episode number

    def __init__(self, name, volume, episode):
        self.name, self.volume, self.episode = name, volume, episode


class bes:
    metadata: Episode_Metadata
    pages: list[Page]

    def __init__(self):
        self.pages = []

    def export(self, out):
        shutil.rmtree("temp_bps")
        os.makedirs("temp_bps")
        for idx, pag in enumerate(self.pages):
            pag.export(f"temp_bps/{idx:02d}.bps")
        os.makedirs(out, exist_ok=True)
        with zipfile.ZipFile(f"{out}/{self.metadata.episode:03d}.bes", 'w', 14) as beszip:
            beszip.comment = b"Created by PSD Interpretter toolkit"
            beszip.writestr("metadata.json", json.dumps(self.metadata.__dict__, ensure_ascii=False))
            for idx, pag in enumerate(self.pages):
                beszip.write(f"temp_bps/{idx:02d}.bps", f"{pag.language}/{idx:02d}.bps")
