import os
import sys
import pathlib
from PIL import Image

# Given some list of file strings to pngs, combine them into a grid N images wide, assuming they are all of the same size.
# filestr_list: list of strings of paths to pngs
# n: number of images to be placed along x
# filestr: output file string without extension
def get_png_grid(dirpath, files_fullpath, output, n):
    images = [Image.open(f) for f in files_fullpath]
    widths, heights = zip(*(i.size for i in images))

    width = widths[0]
    height = heights[0]
    num_y = ((len(files_fullpath) - (len(files_fullpath) % n)) / n)
    new_im = Image.new('RGB', (int(width * n), int(height * num_y)))

    for i, im in enumerate(images):
        x_offset = int(width * (i % n))
        y_offset = int(height * ((i - (i % n)) / n))
        new_im.paste(im, (x_offset, y_offset))

    new_im.save(str(dirpath / output))

def get_png_grid_specific(dirpath):
    files = os.listdir(dirpath)

    names = ['dup.png', 'fak.png', 'eff.png']
    dup = ['duplicationRate_vs_eta.png', 'duplicationRate_vs_phi.png', 'duplicationRate_vs_pT.png']
    fak = ['fakerate_vs_eta.png', 'fakerate_vs_phi.png', 'fakerate_vs_pT.png']
    eff = ['trackeff_vs_eta.png', 'trackeff_vs_phi.png', 'trackeff_vs_pT.png']

    for i, row in enumerate([dup, fak, eff]):
        row_full = [dirpath / png for png in row]
        get_png_grid(dirpath, row_full, names[i], 3)
