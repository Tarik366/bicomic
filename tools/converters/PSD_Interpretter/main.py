import PSDManager as PSDManager
import filesystem as fs
import argparse

parser = argparse.ArgumentParser()

def create_episode(path, output, episode = 0, volume = 0, name = ""):
    print("creating episode:")
    bs = fs.bes()

    def tokenized_pages():
        for i, page_path in enumerate(fs.folder_list_ext_spec(path, ".psd")):
            # TODO: make logging more understandable
            print(page_path)
            yield PSDManager.read_psd_and_tokenize(page_path, i)

    bs.metadata = fs.Episode_Metadata(name, volume, episode)

    bs.export(output, tokenized_pages())

create_episode("example", ".out", 5, 1, "Demek sonumuz bu ha?")
