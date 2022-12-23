import uproot
import json
import os
import pathlib
from matplotlib import pyplot

study_dir = pathlib.Path('2022-12-21-19-20-29')
root_file_list = []

with open(study_dir / 'root_file_list.json') as root_file_list_file:
    root_file_list = json.load(root_file_list_file)

# This is going to get annoying when we have a variety of changing
# values that contribute to a reconstruction algorithm's "score."
# Turn this into a dict or something. This is intuitive for now.
eff_particles_list = []
fakerate_tracks_list = []
duplicaterate_tracks_list = []

for root_file in root_file_list:
    root_path = pathlib.Path(root_file)
    root_dict = uproot.open(root_path)
    print(root_dict)
    eff_particles_list.append(root_dict["eff_particles"].member("fElements")[0])
    fakerate_tracks_list.append(root_dict["fakerate_tracks"].member("fElements")[0])
    duplicaterate_tracks_list.append(root_dict["duplicaterate_tracks"].member("fElements")[0])

# Cool. We can plot the output of each trial's
# CKF performance analyzer. Now run 300
# trials or so. But I don't have enough disk
# space for all those .root files. So I need
# to modify my code to selectively save data.
# Sigh. There is certainly such as thing
# as too much data.

pyplot.rcParams['font.family'] = 'Times New Roman'

figure = pyplot.figure()
figure.set_size_inches(4, 4)
ax = figure.add_subplot()
ax.set_title('eff_particles')
ax.set_xlabel('Number of trials')
ax.set_ylabel('eff_particles')
ax.plot(eff_particles_list)
pyplot.savefig('ap.png', bbox_inches = 'tight', dpi = 300)
