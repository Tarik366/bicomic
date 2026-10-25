import click
import ebooklib
import ebooklib.epub as pub
from languages import Text
import pycountry

""" Main CLI Endpoint, can be fragmented like epub tools and cbz files and moved to the parent"""

# TODO: Make the command names harmonize with them
# TODO: Make an option to use `n` layers to be in base folder. 
# And In future we can add a layer comparator that compare layers of other languages and put to base if they are identical or likely(with some margin of error) the same
# TODO: We can add an option that rasterize neighbor pixel layers too. 

@click.group()
def cli():
    """This script processes a bunch of epub file to single bicomic file that can be interchangebly readible.

    Example:

    \b
        epcomic to_bc example-tr.epub example-en.epub output/  
        epcomic to_epub -r example.bicomic 
    """

@cli.command("to_bc")
@click.argument("epub", nargs=-1, type=click.Path(resolve_path=True))
@click.argument("dest", type=click.Path(resolve_path=True))
@click.option("--rasterize", "-r", is_flag=True, help="Rasterizes all pages to an image. Consumes more storage and complicates translating.")
@click.option("--manual", "-m", help="Allow to manually selecting the languages of files")
def to_bicomic(epub, dest, rasterize, manual):
    """Converts epub files to a bicomic file. Allows multiple files. It looks for language data of epub files. If there's conflicts solved within runtime cli."""
    lang_allocation = Text()
    bes_langs = Text()
    for ind, epub_path in enumerate(epub):
        # open the file
        book = pub.read_epub(epub_path)

        # check the language and compare to previous ones and allocate to lang_allocation variable
        # NOTE: This line might cause some issues with other epub files, must be tested
        book_lang = pycountry.languages.get(alpha_2=book.get_metadata("DC", "language")[0][0]).alpha_3
        print(book_lang)
        if book_lang in lang_allocation.keys():
            # TODO: Move conflicting file to new assigned language and start processing new file to assigned language

            old_conclusion = click.prompt(f"\033[33m Warning: Collusion!\n occured in \"{epub_path}\" and \"{lang_allocation[book_lang]}\". \nWhich language would you like to be assigned to \"{lang_allocation[book_lang]}\"? \033[00m", type=str, default=book_lang)
            new_conclusion = click.prompt(f"\033[33m Warning: Collusion!\nWhich language would you like to be assigned to \"{epub_path}\"? \033[00m", type=str, default=book_lang)
        lang_allocation[book_lang] = epub_path

@cli.command("to_epub")
@click.argument("bicomic", type=click.Path(resolve_path=True))
@click.argument("dest", type=click.Path(resolve_path=True))
@click.option("--rasterize", "-r", is_flag=True, help="Rasterizes all pages to an image. Consumes more storage.")
@click.option("--lang", "-l", default="all", help="Specify languages that will be extracted, languages can be separated with semi-colons. Defaults to 'all' and use ISO 639-3 codes")
def to_epub(count, name):
    """Converts bicomic files to epub files."""
    for x in range(count):
        click.echo(f"Hello {name}!")

@cli.command("add_ep2bicomic")
def add_ep2bicomic():
    """Add one episode to bicomic file"""

@cli.command("to_cbz")
def to_cbz():
    """Converts individuals .bes files or .bes files in .bicomic file to a folder of cbz files"""
    pass

@cli.command("to_bes")
def to_bes():
    pass

@cli.command()
def psd2bicomic():
    """TODO: Move PSD_Interpreter/main.py to here"""

@cli.command()
def bicomic2psd():
    """TODO: reverse of PSD_Interpreter/main.py """

if __name__ == '__main__':
    cli()


"""
import filesystem as fs
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--create-volume", help="Creates a .bicomic Volume file from given directory")
parser.add_argument("-b", "--create-episode", help="Creates a .bes Episode file from given directory")
parser.add_argument("-p", "--create-page", help="Creates a .bps Page file from given psd file")
sub = parser.add_subparsers(dest="command", required=True)

# --to bicomic arguments
volume_args = sub.add_parser("volume")
volume_args.add_argument("book_name")
volume_args.add_argument("volume_n", type=int)

# --create-page arguments

args = parser.parse_args()

def convert_to_bicomic(path, output):
    print("creating episode:")
    bs = fs.bes()

    def tokenized_pages():
        for i, page_path in enumerate(fs.folder_list_ext_spec(path, ".psd")):
            print(page_path)
            yield PSDManager.read_psd_and_tokenize(page_path, i)

    bs.metadata = fs.Episode_Metadata(name, volume, episode)

    bs.export(output, tokenized_pages())

if args.command == "episode":
    create_episode(args.input_folder, args.output_folder, args.episode_n, args.volume_n, args.episode_name)
"""