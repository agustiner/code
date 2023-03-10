import get_efficiency_per_trial
import get_efficiency_pngs
import get_png_grid
import get_study
import get_time
import pathlib

# Get all png files to analyze one optimization.
def get_pngs_optimization(data_dirstr):
    data_dirpath = pathlib.Path(data_dirstr)
    study = get_study.get_study(data_dirpath)
    best_trial = study.best_trial
    best_trial_n = best_trial.number
    best_trial_root_path = data_dirpath / ('trial_' + str(best_trial_n)) / 'performance_ckf.root'
    get_efficiency_pngs.get_efficiency_pngs(best_trial_root_path)
    get_study.get_score_png(data_dirpath)
    get_study.get_parameter_per_trial(data_dirpath)
    get_efficiency_per_trial.get_efficiency_per_trial(data_dirpath)
    get_time.get_time(data_dirpath)

# Get all png files to analyze on sequence.
def get_pngs_single(data_dirstr):
    data_dirpath = pathlib.Path(data_dirstr)
    get_efficiency_pngs.get_efficiency_pngs(data_dirpath / 'performance_ckf.root')
    get_efficiency_pngs.get_efficiency_pngs_combined([str(data_dirpath), '/home/user1/time/2023-02-23/2023-02-23-11-14'], ['Optimized', 'Default'])
