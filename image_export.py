import os
from pathlib import Path
from colorama import Fore, Style

from psd_tools import PSDImage
from helpers import input_directory, directory_exists, psd_name

"""
    Exports images from a photoshop file
    
"""

def save_image(image, size, count):
    if len(count) <= 9:
        image.convert('RGB').save(
            Path(user_directory).joinpath('images', f'{name_pattern}_{size}_0{str(len(count))}.jpg'), quality=85)

    if len(count) > 9:
        image.convert('RGB').save(
            Path(user_directory).joinpath('images', f'{name_pattern}_{size}_{str(len(count))}.jpg'), quality=85)


def filter_layers(artboard, count):
    size = artboard.width
    try:
        for layer in reversed(list(artboard.descendants())):
            if 'image'.lower() in layer.name.lower() \
                and layer.kind == 'group' \
                    and layer.visible:
                try:
                    count.append(layer)
                    image = layer.compose()
                    save_image(image, size, count)

                except AttributeError:
                    pass
    except AttributeError:
        pass

if __name__ == "__main__":
    user_directory = input_directory(message='File path:')

    psd_name = psd_name(user_directory, message='PSD name (can be blank):')

    path_of_psd = Path(user_directory).joinpath(psd_name)

    name_pattern = input('Naming convention (2019-01-01_SS19_C1_GG_Gender): \n')

    print(f'\nLoading {psd_name}')
    psd_load = PSDImage.open(path_of_psd)
    print(f'Finished loading {psd_name}\n')

    os.makedirs(Path(user_directory).joinpath('images'), exist_ok=True)

    print('Exporting images...')
    for layer in reversed(list(psd_load)):
        count=[]
        filter_layers(layer, count)
    print('Done.')
