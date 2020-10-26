import urllib.request
import bs4 as bs
from google_images_download import google_images_download
from shutil import copyfile
from os.path import isdir, exists, split, join
from os import rename, mkdir

#### DOES NOT WORK AS THE PACKAGE google_images_download DOES NOT WORK ANYMORE

response = google_images_download.googleimagesdownload()
images_path = ".\\Images\\"

species_to_download = [
    "Magnolia warbler",
    "Mourning dove"
]

arguments = {
    "keywords": "",
    "limit": 3
}

for species in species_to_download:

    arguments["keywords"] = species
    paths = response.download(arguments)
    # First check if species has a folder
    if not isdir(images_path + species):
        mkdir(images_path + species)
    species_path = images_path + species + "\\"
    if list(paths[0].values())[0]:
        for path in paths[0].values():
            # Determine name of file
            i = 0
            while True:
                i += 1
                species_name_split = species.lower().split(" ")
                filename = "_".join(species_name_split) + str(i) + ".jpg"
                if not exists(species_path + filename):
                    download_path = split(path)[0] + filename
                    rename(path, download_path)
                    copyfile(download_path, species_path + filename)
