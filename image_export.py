import os
from pathlib import Path
from tqdm import tqdm
from typing import List, Tuple

from compression import ImageOptimCompression
from helpers import *

from psd_tools import PSDImage

try:
    if __name__ == "__main__":
        import config
except:
    import setup
    import config

"""
    Exports images from a photoshop file

"""

def filter_image_layers(
    artboard: "psd_tools.api.layers.Artboard", width: str, images: list
) -> list:
    n = []
    try:
        for group in reversed(list(artboard.descendants())):
            if group.kind == "group" and group.visible:
                for layer in reversed(list(group)):
                    if (
                        "image".lower() in layer.name.lower()
                        and layer.kind == "group"
                        and layer.visible
                    ):
                        n.append(1)
                        images.append((layer, width, len(n)))

        return images

    except AttributeError as e:
        print(e)
    except TypeError as e:
        print(e)


if __name__ == "__main__":
    user_directory = valid_directory(message="File path:")

    psd_name = psd_name(
        user_directory, message="PSD name (can be blank or without file extension):"
    )

    path_of_psd = Path(user_directory).joinpath(psd_name)

    user_input = input("Naming convention (2019-01-01_SS19_C1_GG_Gender): \n")
    naming_convention = add_underscore_is_missing(user_input)

    output = Path(user_directory).joinpath("images")
    os.makedirs(output, exist_ok=True)

    print(f"\nLoading {psd_name}")
    psd_load = PSDImage.open(path_of_psd)

    images: List[Tuple] = []
    for artboard in reversed(list(psd_load)):
        width = convert_width_if_email(str(artboard.width))
        filter_image_layers(artboard, width, images)

    """ Instantiate an object for us to upload """
    compress = ImageOptimCompression(username=config.username, path=output)

    print("\nSaving images out with Python Imaging Library...\n")
    for layer, width, n in images:
        """ Save an image at 50% the dimensions for emails (hero module) """
        if 'hero'.lower() in layer.parent.name.lower() and 'desktop'.lower() in width.lower():
            name = image_name_ext_nonretina(width, n)
            save_image_halfsize(layer.parent, layer, name, output)

        name = image_name_ext(naming_convention, width, n)
        save_image(layer, name, output)
        
        if compress.connection_status():
            print(f"Compressing {name} with ImageOptim API")
            """ Uploads file in memory """
            # compress.upload_io(layer, name)

            """ Uploads file from disk """
            compress.upload_file(output, name)
        else:
            print(f"\{name} has not been compressed.")
