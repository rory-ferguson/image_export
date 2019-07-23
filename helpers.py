import os
from pathlib import Path


def psd_name(path: str, message: str):
    user_input = input(f'{message}\n')
    if user_input:
        if directory_exists(path):
            for file in os.listdir(path):
                if user_input in file:
                    return file

    if not user_input:
        for file in os.listdir(path):
            if '.psb' in file or '.psd' in file:
                return file


def valid_directory(message: str) -> str:
    while True:
        try:
            path = f'{message}\n'
        except ValueError:
            print('Invalid path, try again.')
            continue
        if not directory_exists(path):
            continue            
        else:
            break
    return path


def directory_exists(path: str) -> bool:
    try:
        if os.path.exists(os.path.dirname(path)):
            return True
        else:
            return False
    except TypeError:
        pass


def decimal_count(count: int) -> str:
    if count <= 9:
        return f'0{count}'
    else:
        return f'{count}'


def underscore(pattern: str) -> str:
    if not pattern:
        return pattern
    elif '_' in pattern and len(pattern) > 1:
        return ''
    elif '_' in pattern[-1:]:
        return pattern
    elif '_' not in pattern[-1:]:
        return f'{pattern}_'


def convert_width_if_email(width: str) -> str:
    if width == '850':
        return 'Mobile'
    elif width == '1280':
        return 'Desktop'
    else:
        return
