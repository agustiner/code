from matplotlib import pyplot
import os
import pathlib
import pandas
import get_figure

def starts_with_trial(s):
    return s.startswith('trial_')

def get_trial_path_from_str(s, d):
    return pathlib.Path(d) / s

def get_time_trial(trial_path):
    timing_path = trial_path / 'timing.tsv'
    timing = pandas.read_csv(timing_path, sep="\t")
    time_ckf = float(
        timing[timing["identifier"].str.match("Algorithm:TrackFindingAlgorithm")][
            "time_perevent_s"
        ]
    )
    time_seeding = float(
        timing[timing["identifier"].str.match("Algorithm:SeedingAlgorithm")][
            "time_perevent_s"
        ]
    )
    cur_runtime = time_ckf + time_seeding
    return cur_runtime

def get_time(data_dirpath):
    time_trials = []
    listdir = os.listdir(data_dirpath)
    trial_paths = []
    for dir in listdir:
        if starts_with_trial(dir):
            trial_paths.append(data_dirpath / dir)
            
    for trial_path in trial_paths:
        time_trials.append(get_time_trial(trial_path))
        
    figure = get_figure.get_study_figure(time_trials, 'Trial', '', 'Run time per trial [s]')
    pyplot.savefig(data_dirpath / 'time.png', dpi = 200)
