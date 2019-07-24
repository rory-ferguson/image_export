import sys
import os
import requests
import logging
from pathlib import Path

logging.captureWarnings(True)


class ImageOptimCompression(object):

    def __init__(self, username, path):
        self.endpoint = 'https://im2.io'
        self.username = username
        self.quality = 'full'

        self.path = Path(path)
        self.url = self.build_url()

    def build_url(self):
        url_parts = [
            self.endpoint,
            self.username,
            self.quality
        ]
        return '/'.join(url_parts)
    
    def _image(self, name):
        path = Path(self.path).joinpath(name)
        if os.path.exists(path):
            self.image_path = path
        else:
            sys.exit(f'{name} not found in {self.path}')

    def request(self, name):
        self._image(name)
        print(name)
        files = {'upload_file': open(self.image_path, 'rb')}

        try:
            self.r = requests.post(str(self.url), files=files, stream=True, verify=False)
            self.r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        self._save()
    
    def _save(self):
        with open(self.image_path, 'wb') as fd:
            for chunk in self.r.iter_content(chunk_size=1048):
                fd.write(chunk)
