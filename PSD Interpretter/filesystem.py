import os, zipfile

from Page.bcs_tokenizer import Page

def folder_list(path):
    f = []
    # TODO: Sort numbers correctly
    for (dirpath, dirnames, filenames) in os.walk(path):
        for files in (filenames):
            f.append(f"{dirpath}/{files}")
        break
    return f

def folder_list_ext_spec(path, ext = ".bcs"):
    f = []
    for file in folder_list(path):
        if file.endswith(ext):
            f.append(file)
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

import shutil

class bes:
    metadata: Episode_Metadata
    pages: list[Page]

    def __init__(self):
        self.pages = []

    # TODO: Make the `.bes` file export
    def export(self, out):
        shutil.rmtree("temp_bps")
        print(self.pages)
        print(self.pages[0].lines.__len__())
        os.makedirs("temp_bps")
        for idx, pag in enumerate(self.pages):
            pag.export(f"temp_bps/{idx:02d}.bps")
        os.makedirs(out, exist_ok=True)
        with zipfile.ZipFile(f"{out}/{self.metadata.episode:03d}.bes", 'w') as beszip:
            beszip.comment = self.metadata.__dict__.__str__().encode()
            for idx, pag in enumerate(self.pages):
                beszip.write(f"temp_bps/{idx:02d}.bps", f"{pag.language}/{idx:02d}.bps")
