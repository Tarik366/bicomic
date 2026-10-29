from filesystem import *
from bcs_tokenizer import *
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

import ebooklib
import ebooklib.epub as pub

def process_pages(pages):
    for idx, item in enumerate(pages):
        # TODO: Don't forget to add include styles from internal and external sources
        match item.get_type():
            case ebooklib.ITEM_DOCUMENT:
                page = bs(item.get_content(), "lxml-xml")
                for lines_in_page in page.body.contents:
                    print(lines_in_page)
                    
                
        
def epub_table_to_bicomic(lang_allocation) -> bicomic:
    """Main loop for processing epub files and creating bicomic format"""
    for ind, (epub_file_lang, epub_file_path) in tqdm(enumerate(lang_allocation.items())):
        epub = pub.read_epub(epub_file_path)

        process_pages(epub.get_items())
        
        
        print(ind)

epub_table_to_bicomic({"eng": "epub interpretter/exam.epub"})