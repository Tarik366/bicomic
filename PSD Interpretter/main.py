import Page.PSDManager as PSDManager
import filesystem as fs
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--create-volume", help="Creates a .bcz Volume file from given directory")
parser.add_argument("-e", "--create-episode", help="Creates a .bes Episode file from given directory")
parser.add_argument("-p", "--create-page", help="Creates a .bps Page file from given psd file")
sub = parser.add_subparsers(dest="command", required=True)

# --create-volume arguments
volume_args = sub.add_parser("volume")
volume_args.add_argument("book_name")
volume_args.add_argument("volume_n", type=int)

# --create-episode arguments
episode_args = sub.add_parser("episode")
episode_args.add_argument("input_folder")
episode_args.add_argument("output_folder")
episode_args.add_argument("episode_n", type=float)
episode_args.add_argument("episode_name")

# --create-page arguments

args = parser.parse_args()

# TODO: Make a Command Line Interface

def create_episode(path, output, episode = 0, volume = 0, name = ""):
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
