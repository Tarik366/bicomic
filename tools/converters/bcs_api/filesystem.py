import os, zipfile, json, tempfile, re, datetime
from collections.abc import Iterable
import PIL.Image

from bcs_tokenizer import Page
from languages import Text, Age_Rating, Demographic, Publication, Format

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
    return f

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

    # credits
    author: str
    artist: str

    publisher: str

    # Translation credits
    translator: Text # language specific and can be comma seperated
    cleaners: Text
    typesetters: Text
    quality_check: Text
    proofreaders: Text

    demographic: Demographic | None # Target demographic
    genres: list
    format: list[Format]
    content_rating: Age_Rating # Minimum allowed age

    release_date: datetime.date
    publication_status: Publication

    def __init__(self, dict, /, **kwds):
        for key in dict:
            setattr(self, key, dict[key])
        for key in kwds:
            setattr(self, key, kwds[key])

class bes:
    metadata: Episode_Metadata | None
    serie_metadata: Serie_Metadata | None
    pages: list[Page]

    def __init__(self, dict = {}, /, **kwds):
        self.pages = []
        # Make someway to share metadatas between episode and serie or create a combined class of two 
        for key in dict:
            setattr(self.metadata, key, dict[key])
        for key in kwds:
            setattr(self.metadata, key, kwds[key])

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

class bicomic:
    metadata: Serie_Metadata
    covers: list[PIL.Image.Image]
    episodes: list[bes]

    volume: int
    
    def __init__(self, volume = 1):
        self.metadata = Serie_Metadata()
        self.cover = None
        self.episodes = []
        self.volume = volume

    # TODO: You forget here
    def export(self, out):
        os.makedirs(out, exist_ok=True)
        output_path = os.path.join(out, f"{self.metadata.episode:003.0f}.bes")

