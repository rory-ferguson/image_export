import os
from pathlib import Path
from tqdm import tqdm

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

def filter_layers(artboard: 'psd_tools.api.layers.Artboard', count: list, pattern: str, user_directory: str, size: str, output: 'pathlib.WindowsPath'):
    try:
        for layer in reversed(list(artboard.descendants())):
            if layer.kind == 'group':
                if 'image'.lower() in layer.name.lower() \
                    and layer.kind == 'group' \
                        and layer.visible:
                    count.append(layer)
                    image = layer.compose()
                    name = save_image(image, size, len(count), pattern, user_directory, output)
                    compress.request(name)
                    
    except AttributeError as e:
        print(e)
    except TypeError:
        pass

def save_image(image: 'PIL.Image.Image', size: str, count: int, pattern: str, user_directory: str, output):
    count = decimal_count(count)
    return image.convert('RGB').save(Path(output).joinpath(f'{pattern}{size}_{count}.jpg'), quality=85)


if __name__ == "__main__":
    user_directory = valid_directory(message='File path:')

    psd_name = psd_name(user_directory, message='PSD name (can be blank or without file extension):')

    path_of_psd = Path(user_directory).joinpath(psd_name)

    user_input = input('Naming convention (2019-01-01_SS19_C1_GG_Gender): \n')
    naming_convention = underscore(user_input)

    output = Path(user_directory).joinpath('images')
    os.makedirs(output, exist_ok=True)

    compress = ImageOptimCompression(username=config.username, path=output)

    print(f'\nLoading {psd_name}')
    psd_load = PSDImage.open(path_of_psd)

    print('\nExporting images...')
    for layer in reversed(list(psd_load)):
        count=[]
        size = convert_width_if_email(str(layer.width))
        filter_layers(layer, count, naming_convention, user_directory, size, output)
    print('Done.')
