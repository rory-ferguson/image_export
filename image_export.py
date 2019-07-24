import os
from pathlib import Path
from tqdm import tqdm

from compression import ImageOptimCompression
from helpers import *

from psd_tools import PSDImage

root = os.path.dirname(os.path.abspath(__file__))

"""
    Exports images from a photoshop file
    
"""

def new_psd(path: str, layer: 'psd_tools.api.smart_object.SmartObject') -> 'PIL.Image.Image':
    file_psd = Path(path).joinpath(layer.filename)
    layer.save(file_psd)
    return PSDImage.open(file_psd).compose()


def filter_layers(artboard: 'psd_tools.api.layers.Artboard', count: list, pattern: str, user_directory: str, size: str, output: 'pathlib.WindowsPath'):
    try:
        for layer in reversed(list(artboard)):
            if layer.kind == 'group':
                if 'new in'.lower() in layer.name.lower() \
                    and layer.kind == 'group' \
                        and layer.visible:
                    try:
                        for i in reversed(list(layer.descendants())):
                            if i.kind == 'smartobject' \
                                and 'block'.lower() in i.name.lower() \
                                    and i.visible:
                                count.append(i)
                                layer = i.smart_object
                                image = new_psd(user_directory, layer)
                                name = save_image(image, size, len(count), pattern, user_directory, output)
                                remove_file(user_directory, layer.filename)
                                compress.request(name)
                    except AttributeError:
                        pass
                else:
                    for i in reversed(list(layer.descendants())):
                        if 'image'.lower() in i.name.lower() \
                            and i.kind == 'group' \
                                and i.visible:
                            count.append(i)
                            image = i.compose()
                            name = save_image(image, size, len(count), pattern, user_directory, output)
                            compress.request(name)
            
            filter_layers(layer, count, naming_convention, user_directory, size, output)

    except AttributeError as e:
        print(e)
    except TypeError:
        pass

def save_image(image: 'PIL.Image.Image', size: str, count: int, pattern: str, user_directory: str, output):
    count = decimal_count(count)
    name = f'{pattern}{size}_{count}.jpg'
    image.convert('RGB').save(
        Path(output).joinpath(f'{pattern}{size}_{count}.jpg'), quality=85)
    return name


if __name__ == "__main__":
    user_directory = valid_directory(message='File path:')

    psd_name = psd_name(user_directory, message='PSD name (can be blank or without file extension):')

    path_of_psd = Path(user_directory).joinpath(psd_name)

    user_input = input('Naming convention (2019-01-01_SS19_C1_GG_Gender): \n')
    naming_convention = underscore(user_input)

    output = Path(user_directory).joinpath('images')
    os.makedirs(output, exist_ok=True)
    
    try:
        if __name__ == "__main__":
            import config
        else:
            import config as config
    except:
        print('First time installation requires config.py file.')
        print('Creating config.py...')
        config_file = open(Path(root).joinpath('config.py'), 'w')

        username = input('Whats your ImageOptim API username?')
        config_file.write(f"username='{username}'")
        config_file.close()

        import config

    compress = ImageOptimCompression(username=config.username, path=output)

    print(f'\nLoading {psd_name}')
    psd_load = PSDImage.open(path_of_psd)

    print('\nExporting images...')
    for layer in reversed(list(psd_load)):
        count=[]
        size = convert_width_if_email(str(layer.width))
        filter_layers(layer, count, naming_convention, user_directory, size, output)
    print('Done.')
