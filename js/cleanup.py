# Delete .png files that are not in nodes.json.

import json
import random
import string
import os

files = os.listdir('./')

def ends_with_png(s):
    return s.endswith('png')

files_png = filter(ends_with_png, files)

nodes_file = open('./nodes.json', 'r')
nodes_json = json.load(nodes_file)

for file_png in files_png:
    if file_png not in nodes_json:
        print(file_png, 'not in json, deleting.')
        os.unlink(file_png)

nodes_file.close()
