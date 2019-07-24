import os
from pathlib import Path

root = os.path.dirname(os.path.abspath(__file__))

def setup():
    print('First time installation requires config.py file.')
    print('Creating config.py...')
    config_file = open(Path(root).joinpath('config.py'), 'w')

    username = input('Whats your ImageOptim API username?')
    config_file.write(f"username='{username}'")
    config_file.close()
    print(f'username set as {username}')
setup()