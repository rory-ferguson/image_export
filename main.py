import os
from pathlib import Path
from tqdm import tqdm

from src.compression import ImageOptimCompression
from src.helpers import *
from src.psd import new_psd, save_image, image_name

from collections.abc import Iterable

from psd_tools import PSDImage

try:
    if __name__ == "__main__":
        import config
except:
    from image_export.setup import setup
    import config

"""
    Exports images from a photoshop file
    
"""

def filter_layers(artboard: 'psd_tools.api.layers.Artboard', count: list, pattern: str, user_directory: str, width: str, output):
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
                                print(i)
                                # count.append(i)
                                # layer = i.smart_object
                                # image = new_psd(user_directory, layer)
                                # name = save_image(image, width, len(count), pattern, user_directory, output)
                                # remove_file(user_directory, layer.filename)
                                # compress.request(name)
                    except AttributeError:
                        pass
                else:
                    for i in reversed(list(layer.descendants())):
                        if 'image'.lower() in i.name.lower() \
                            and i.kind == 'group' \
                                and i.visible:
                            print(i)
                            count.append(i)
                            # image = i.compose()
                            # save_image(image, width, len(count), pattern, output)
                            # compress.request(image_name(pattern, width, len(count)))
                            
            
            filter_layers(layer, count, pattern, user_directory, width, output)

    except TypeError:
        pass


def other(artboard: 'psd_tools.api.layers.Artboard', regular: list, embedded: list):
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
                                embedded.append(i)
                    except AttributeError:
                        pass
                else:
                    try:
                        print(layer)
                        for i in reversed(list(layer.descendants())):
                            if 'image'.lower() in i.name.lower() \
                                and i.kind == 'group' \
                                    and i.visible:
                                regular.append(i)
                    except AttributeError as e:
                        print(e)

            other(layer, regular, embedded)

    except AttributeError as e:
        print(e)
        pass
    except TypeError as e:
        pass

if __name__ == "__main__":
    # user_directory = valid_directory(message='File path:')
    user_directory = 'C:\\Users\\rory.ferguson\\Documents\\test\\resources'

    # psd_name = psd_name(user_directory, message='PSD name (can be blank or without file extension):')
    psd_name = 'US_AW19_C4_Mens_R4.psd'

    path_of_psd = Path(user_directory).joinpath(psd_name)

    # user_input = input('Naming convention (2019-01-01_SS19_C1_GG_Gender): \n')
    user_input = ''
    naming_convention = underscore(user_input)

    output = Path(user_directory).joinpath('images')
    os.makedirs(output, exist_ok=True)
    
    compress = ImageOptimCompression(username=config.username, path=output)

    print(f'\nLoading {psd_name}')
    psd_load = PSDImage.open(path_of_psd)

    print('\nExporting images...')
    regular=[]
    embedded=[]
    for layer in reversed(list(psd_load)):
        print(layer)
        # count=[]
        width = convert_width_if_email(str(layer.width))
        filter_layers(layer, count, naming_convention, user_directory, width, output)
        # other(layer, regular, embedded)
    print(embedded)
    # print(regular)
    print('Done.')
