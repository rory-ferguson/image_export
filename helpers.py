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


def input_directory(message):
    while True:
        try:
            path = input(f'{message}\n')
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

