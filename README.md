# Image Exporter

A program to export and compress JPG images from a PSD file.

## Installation

Requires Python 3.6+

Install the dependency packages ([psd-tools](https://github.com/psd-tools/psd-tools), [numpy](https://github.com/numpy/numpy), [scipy](https://github.com/scipy/scipy)) with

``` python
    cd main/
    pip install -r requirements.txt
```

## ImageOptim

The program relies on imageOptim to compress the images, an `account key` is required. [https://imageoptim.com/api](https://imageoptim.com/api).

When initially running the program, a `config.py` will be created and require an input for the `account key`

## How To

Open a terminal inside of the repository

``` terminal
    python main.py
```

After running `python main.py`, input the values relating to the prompts

``` terminal
    File path: C:\\Folder\\
    PSD name (can be blank or without file extension): Example.psd
    Naming convention (2019-01-01_SS19_C1_GG_Gender): Image
```

The images will output to an `images` directory and look similar to the below

- Image_850_01.jpg
- Image_850_02.jpg
- Image_1280_01.jpg
- Image_1280_02.jpg

The `850` and `1280` relate to the artboards width.

## Notes on photoshop data

A group folder called `image` is required and all layers should be nested into this folder.
