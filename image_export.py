import os
from pathlib import Path

from psd_tools import PSDImage
from helpers import valid_directory, directory_exists, psd_name, decimal_count, underscore, convert_width_if_email, input_message

"""
    Exports images from a photoshop file
    
"""

def filter_layers(artboard: 'psd_tools.api.layers.Artboard', count: list, pattern: str):
    try:
        for layer in reversed(list(artboard.descendants())):
            if 'image'.lower() in layer.name.lower() \
                and layer.kind == 'group' \
                    and layer.visible:
                try:
                    count.append(layer)
                    image = layer.compose()
                    save_image(image, size, len(count), pattern)
                except AttributeError:
                    pass
    except AttributeError:
        pass

def save_image(image: 'PIL.Image.Image', size: str, count: int, pattern: str):
    count = decimal_count(count)
    image.convert('RGB').save(
        Path(user_directory).joinpath('images', f'{pattern}{size}_{count}.jpg'), quality=85)


if __name__ == "__main__":
    user_directory = valid_directory(message='File path:')

    psd_name = psd_name(user_directory, message='PSD name (can be blank or without file extension):')

    path_of_psd = Path(user_directory).joinpath(psd_name)

    user_input = input('Naming convention (2019-01-01_SS19_C1_GG_Gender): \n')
    naming_convention = underscore(user_input)

    print(f'\nLoading {psd_name}')
    psd_load = PSDImage.open(path_of_psd)
    print(f'Finished loading {psd_name}\n')

    os.makedirs(Path(user_directory).joinpath('images'), exist_ok=True)
    
    print('Exporting images...')
    for layer in reversed(list(psd_load)):
        count=[]
        size = convert_width_if_email(str(layer.width))
        filter_layers(layer, count, naming_convention)
    print('Done.')
