from pathlib import Path

from psd_tools import PSDImage

from src.helpers import count_to_str
from src.compression import ImageOptimCompression

"""
    Exports images from a photoshop file
"""

def new_psd(path: str, layer: 'psd_tools.api.smart_object.SmartObject') -> 'PIL.Image.Image':
    file_psd = Path(path).joinpath(layer.filename)
    layer.save(file_psd)
    return PSDImage.open(file_psd).compose()

def save_image(image: 'PIL.Image.Image', width: str, count: int, pattern: str, output):
    name = image_name(pattern, width, count)
    image.convert('RGB').save(Path(output).joinpath(name), quality=85)
    return name

def image_name(pattern: str, width: str, count: int):
    return f'{pattern}{width}_{count_to_str(count)}.jpg'
