import os
from pathlib import Path

from typing import Union, Any, List, Optional, cast
from typing import List


def psd_name(path: str, message: str):
    user_input = input(f'{message}\n')
    if user_input:
        if directory_exists(path):
            for file in os.listdir(path):
                if user_input in file:
                    return file

    if not user_input:
        if directory_exists(path):
            for file in os.listdir(path):
                if '.psb' in file or '.psd' in file:
                    return file


def valid_directory(message: str) -> str:
    while True:
        try:
            path = input(f'{message}\n')
        except ValueError:
            continue
        if not directory_exists(path):
            print('Invalid path, try again.')
            continue
        else:
            break
    return path


def directory_exists(path: str) -> bool:
    if os.path.exists(os.path.dirname(path)):
        return True
    return False


def decimal_count(count: int) -> str:
    if isinstance(count, int):
        if count <= 9:
            return f'0{count}'
        else:
            return f'{count}'


def add_underscore_is_missing(pattern: str) -> str:
    if not pattern:
        return pattern
    elif '_' not in pattern[-1:]:
        return f'{pattern}_'
    return pattern


def convert_width_if_email(width: str) -> str:
    if width == '850':
        return 'Mobile'
    elif width == '1280':
        return 'Desktop'
    else:
        return width


def image_name_ext(pattern: Any, width: str, count: Any) -> str:
    count = decimal_count(count)
    return f'{pattern}{width}_{count}.jpg'


def save_image(layer: 'PIL.Image.Image', name: str, output):
    print(name)
    image = layer.compose()
    image.convert('RGB').save(
        Path(output).joinpath(name), quality=85)