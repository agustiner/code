from matplotlib import pyplot
import ROOT
import pathlib
import get_study
import get_figure
import os

def starts_with_trial(s):
    return s.startswith('trial_')

def get_root_from_trial_str(s):
    trial_path = pathlib.Path(s)
    root_path = trial_path / 'performance_ckf.root'
    return root_path

def get_score_keys():
    return ['duplicaterate_particles', 'duplicaterate_tracks', 'eff_particles', 'eff_tracks', 'fakerate_particles', 'fakerate_tracks']

# root_path: Path
# Get the particle eff, track eff, particle dup, track dup, particle fake, track fake, as function of trial. Save each as a png.
def get_efficiency_per_trial(study_dirpath):
    list = os.listdir(study_dirpath)
    trial_dirs = filter(starts_with_trial, list)
    root_paths = map(get_root_from_trial_str, trial_dirs)
    score_keys = get_score_keys()
    score_dict = {}
    
    # Set the keys to be empty.
    for score_key in score_keys:
        score_dict[score_key] = []

    for root_path in root_paths:
        tfile = ROOT.TFile.Open(str(study_dirpath / root_path))

        for score_key in score_keys:
            score_dict[score_key].append(tfile.Get(score_key)[0])

    for score_key in score_keys:
        fig = get_figure.get_study_figure(score_dict[score_key], 'Trial', '', score_key)
        eff_path = study_dirpath / 'efficiency_per_trial'        
        if (eff_path.exists() == False):
            os.mkdir(eff_path)
            
        pyplot.savefig(eff_path / score_key, bbox_inches='tight', dpi = 200)
        
    path = study_dirpath / 'efficiency_per_trial'
    points = [score_dict[score_key] for score_key in score_keys]
    xlabels = ['Trial' for i in range(len(score_keys))]
    get_figure.get_grid(3, 2, points, xlabels, score_keys, path)
