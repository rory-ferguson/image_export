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
                for layer in reversed(list(group.descendants())):
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

    compress = ImageOptimCompression(username=config.username, path=output)

    if compress.connection_status():
        print("\nExporting images... with ImageOptim\n")
        for layer, width, n in images:
            name = image_name_ext(naming_convention, width, n)

            """ Uploads file in memory 
            compress.upload_io(layer, name)
            """

            """ Uploads file from disk """
            save_image(layer, name, output)
            compress.upload_file(output, name)
    else:
        print("\nImageOptim is down! Savings images out with PIL\n")
        for layer, width, n in images:
            name = image_name_ext(naming_convention, width, n)
            print(name)
            save_image(layer, name, output)
        input("\nWARNING, remember to compress the images...")
