import Page.PSDManager as PSDManager
import filesystem as fs

fafa = PSDManager.read_psd_and_tokenize("unicorn-controller.psd")

print(fafa)

fafa.export("fal.zip")

print(fs.folder_list("sample"))

bs = fs.bes()

bs.metadata = fs.Episode_Metadata("tur", 24, "Bir dakikanı rica edebilir miyim?", 3, 36)

bs.export()

# TODO: Make a Command Line Interface
