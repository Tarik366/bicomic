import os, zipfile, json, tempfile, re, datetime
from collections.abc import Iterable
import PIL.Image
from manga_updates_api_client import Client
from manga_updates_api_client.api.series import retrieve_series

from Page.bcs_tokenizer import Page
from languages import Text, Age_Rating, Demographic, Publication

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

class Serie_Metadata:
    titles: Text
    descriptions: Text
    author: str
    artist: str

    isbn: int # 13-digit number that identify the book

    demographic: Demographic
    genres: list
    format: str
    content_rating: Age_Rating # Minimum allowed age

    release_date: datetime.date
    publication_status: Publication

    def __init__(self, title: Text, description: Text, author, artist):
        pass

class bes:
    metadata: Episode_Metadata
    pages: list[Page]

    def __init__(self):
        self.pages = []

    def export(self, out, pages: Iterable[Page] | None = None):
        os.makedirs(out, exist_ok=True)
        output_path = os.path.join(out, f"{self.metadata.episode:003.0f}.bes")

        with tempfile.TemporaryDirectory(prefix=".bicomic-export-", dir=out) as work_dir:
            archive_path = os.path.join(work_dir, "episode.bes")
            page_path = os.path.join(work_dir, "page.bps")
            with zipfile.ZipFile(archive_path, "w", 14) as beszip:
                beszip.comment = b"Created by PSD Interpretter toolkit"
                beszip.writestr("metadata.json", json.dumps(self.metadata.__dict__, ensure_ascii=False))
                page_iter = iter(self.pages if pages is None else pages)
                idx = 0
                while True:
                    try:
                        pag = next(page_iter)
                    except StopIteration:
                        break
                    pag.export(page_path)
                    beszip.write(page_path, f"{pag.language}/{idx:02d}.bps")
                    # Release the current page before the iterator constructs the next one.
                    del pag
                    idx += 1

            os.replace(archive_path, output_path)

class bcz:
    metadata: Serie_Metadata
    # TODO: Make some way to add multi-lingual covers. 
    cover: PIL.Image.Image
    episodes: list[bes]
    
    def __init__(self):
        self.metadata = Serie_Metadata()
        self.cover = None
        self.episodes = []
