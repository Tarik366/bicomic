import os, zipfile

from Page.bcs_tokenizer import Page

def folder_list(path):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        f.extend(filenames)
        break
    return f

class bcz:
    def __init__(self):
        with zipfile.ZipFile('spam.zip', 'w') as myzip:
            myzip.comment = "bu bir test dosyasıdır ve çıkışa yakın düzeltilmelidir".encode()
            myzip.write('export.bcs')
            myzip.close()

class Episode_Metadata:

    language = ""
    page_count = 0

    # Episode details
    name = ""     # Episode name
    volume = 0    # Volume that contain this episode
    episode = 0   # Episode number

    def __init__(self, language, pages, name, volume, episode):
        self.language, self.page_count, self.name, self.volume, self.episode = language, pages, name, volume, episode

class bes:
    metadata: Episode_Metadata
    pages: list[Page]

    # TODO: Make the `.bes` file export
    def export(self):
        for idx, pag in enumerate(self.pages):
            pag.export(f"temp_bps/{idx:02d}.bps")
        with zipfile.ZipFile(f"{self.metadata.episode:03d}.bes", 'w') as beszip:
            beszip.comment = self.metadata.__dict__.__str__().encode()
            for idx, pag in enumerate(self.pages):
                beszip.write(f"temp_bps/{idx:02d}.bps", )
