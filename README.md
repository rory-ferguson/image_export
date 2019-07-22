# Image Exporter

A script to export JPG images from a PSD file.

## Installation

Requires Python 3.6+

Install the dependency packages ([psd-tools](https://github.com/psd-tools/psd-tools), [numpy](https://github.com/numpy/numpy), [scipy](https://github.com/scipy/scipy))

``` python
    pip install -r requirements.txt
```

## How To

``` terminal
    cd image_export/
    pip install -r requirements.txt
    python image_export.py
```

After running `python image_export.py` input the values relating to the prompts shown below;

``` terminal
    File path: C:\\Folder\\
    PSD name: Example.psd
    Naming convention: Image
```

The images will output to an `images` directory and look like the below

- Image_850_01.jpg
- Image_850_02.jpg
- Image_1280_01.jpg
- Image_1280_02.jpg

The `850` and `1280` related to the artboards width.

## Notes on photoshop data

A group folder called `image` is required and all layers should be nested into this folder.
