import uproot
import json
import os
import pathlib
import matplotlib
from matplotlib import pyplot

def plot_xyz(xstring, ystring, zstring, titlestring, xarray, yarray, zarray):
    # Plot an x-y-z graph.
    pass

def plot_xy(xstring, ystring, titlestring, xarray, yarray):
    # Plot an x-y graph.
    pass

def plot_array(xstring, ystring, titlestring, array):
    # Plot one array.
    
    pyplot.rcParams['font.family'] = 'Times New Roman'
    figure = pyplot.figure()
    figure.set_size_inches(6, 3)
    ax = figure.add_subplot()
    ax.set_ylabel(ystring)
    ax.set_xlabel(xstring)
    ax.set_title(titlestring)
    ax.plot(array)

    for axi in pyplot.gcf().axes:
        axi.get_lines()[0].set_color('black')

    for axic in ax.get_children():
        if isinstance(axic, matplotlib.spines.Spine):
            axic.set_color('black')

    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
        
    pyplot.savefig(titlestring + '.png', bbox_inches = 'tight', dpi = 200)
    
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


plot_array('Number of trials', 'Particle efficiency', 'Particle efficiency', eff_particles_list)
plot_array('Number of trials', 'Track fake rate', 'Track fake rate', fakerate_tracks_list)
plot_array('Number of trials', 'Track duplicate rate', 'Track duplicate rate', duplicaterate_tracks_list)
