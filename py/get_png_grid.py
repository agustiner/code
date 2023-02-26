import os
import sys
import pathlib
from PIL import Image

# Given some list of file strings to pngs, combine them into a grid N images wide, assuming they are all of the same size.
# filestr_list: list of strings of paths to pngs
# n: number of images to be placed along x
# filestr: output file string without extension
def get_png_grid(dirpath, n):
    files = os.listdir(dirpath)
    files_full = [dirpath / f for f in files]
    images = [Image.open(f) for f in files_full]
    widths, heights = zip(*(i.size for i in images))

    width = widths[0]
    height = heights[0]
    num_y = ((len(files) - (len(files) % n)) / n)
    new_im = Image.new('RGB', (int(width * n), int(height * num_y)))

    for i, im in enumerate(images):
        x_offset = int(width * (i % n))
        y_offset = int(height * ((i - (i % n)) / n))
        new_im.paste(im, (x_offset, y_offset))

    new_im.save(str(dirpath / 'grid.png'))
