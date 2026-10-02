import Page.PSDManager as PSDManager
import filesystem as fs
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-e", "--create-episode", help="Creates a .bes file from given directory")

parser.parse_args()

# TODO: Make a Command Line Interface

def create_episode(path, output, episode = 0, volume = 0, name = ""):
    print("creating episode:")
    bs = fs.bes()
    
    for i, pages in enumerate(fs.folder_list_ext_spec(path, ".psd")):
        print(pages)
        bs.pages.append(PSDManager.read_psd_and_tokenize(pages, i))
        
    bs.metadata = fs.Episode_Metadata(name, volume, episode)

    bs.export(output)

create_episode("example", "test", 36, 3, "Bir dakikanı rica edebilir miyim?")