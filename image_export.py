import os
from pathlib import Path

from psd_tools import PSDImage
from helpers import valid_directory, directory_exists, psd_name, decimal_count, underscore, convert_width_if_email, remove_file

"""
    Exports images from a photoshop file
    
"""

def new_psd(path: str, layer: 'psd_tools.api.smart_object.SmartObject') -> 'PIL.Image.Image':
    file_psd = Path(path).joinpath(layer.filename)
    layer.save(file_psd)
    return PSDImage.open(file_psd).compose()


def filter_layers(artboard: 'psd_tools.api.layers.Artboard', count: list, pattern: str, user_directory: str, size: str ):
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
                                save_image(image, size, len(count), pattern, user_directory)
                                remove_file(user_directory, layer.filename)
                    except AttributeError:
                        pass
                else:
                    for i in reversed(list(layer.descendants())):
                        if 'image'.lower() in i.name.lower() \
                            and i.kind == 'group' \
                                and i.visible:
                            count.append(i)
                            image = i.compose()
                            save_image(image, size, len(count), pattern, user_directory)
            
            filter_layers(layer, count, naming_convention, user_directory, size)

    except AttributeError:
        pass
    except TypeError:
        pass

def save_image(image: 'PIL.Image.Image', size: str, count: int, pattern: str, user_directory: str):
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

    os.makedirs(Path(user_directory).joinpath('images'), exist_ok=True)
    
    print('\nExporting images...')
    for layer in reversed(list(psd_load)):
        count=[]
        size = convert_width_if_email(str(layer.width))
        filter_layers(layer, count, naming_convention, user_directory, size)
    print('Done.')
