import os
import requests
import logging
from tqdm import tqdm
from pathlib import Path

logging.captureWarnings(True)

if __name__ == "__main__":
    import config
else:
    import config as config


class ImageOptimCompression(object):

    def __init__(self):
        self.endpoint = 'https://im2.io'
        self.username = config.username
        self.quality = 'full'
        self.path = ''
        self.output = ''
        self.url = self.build_url()

    def build_url(self):
        url_parts = [
            self.endpoint,
            self.username,
            self.quality
        ]
        return '/'.join(url_parts)

    def request(self, path, name):
        self.path = Path(path)
        self.output = self.path.joinpath('images')

        image = self.output.joinpath(name)
        files = {'upload_file': open(image, 'rb')}
        
        r = requests.post(str(self.url), files=files, stream=True, verify=False)

        with open(image, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1048):
                fd.write(chunk)
