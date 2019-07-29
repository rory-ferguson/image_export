import sys
import requests
import logging
from pathlib import Path
from io import BytesIO

logging.captureWarnings(True)


class ImageOptimCompression(object):
    def __init__(self, username, path):
        self.endpoint = "https://im2.io"
        self.username = username
        self.quality = "full"

        self.path = Path(path)
        self.url = self._build_url()
        self.image_path = ""

    def _build_url(self):
        url_parts = [self.endpoint, self.username, self.quality]
        return "/".join(url_parts)

    def connect_test(self):
        try:
            r = requests.get(self.endpoint)
            r.raise_for_status()
            return True
        except requests.exceptions.HTTPError:
            return False

    def upload_io(self, layer, name):
        self.image_path = Path(self.path).joinpath(name)

        upload_file = BytesIO()
        image = layer.compose()
        image.convert("RGB").save(upload_file, "JPEG")
        upload_file.seek(0)
        files = {"upload_file": upload_file}
        print(name)
        try:
            self.r = requests.post(
                str(self.url), files=files, stream=True, verify=False
            )
            self.r.raise_for_status()
            self._save()
        except requests.exceptions.HTTPError as e:
            print(e)

    def _save(self):
        with open(self.image_path, "wb") as fd:
            for chunk in self.r.iter_content(chunk_size=1048):
                fd.write(chunk)
