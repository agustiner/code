import get_study
import sequence
import get_time_dir

# Given folder path to
# optimization_dirpath: Path to folder containing study.db
def get_new_simulation_from_optimization(optimization_dirpath):
    study = get_study.get_study(optimization_dirpath)
    best_trial_params = study.best_trial.params
    time_path = get_time_dir.get_time_dir()
    sequence.run(time_path, best_trial_params)

def get_new_simulation_from_default():
    time_path = get_time_dir.get_time_dir()
    default_params = {'maxSeedsPerSpM': 1,
                      'cotThetaMax': 7.40627,
                      'sigmaScattering': 5,
                      'radLengthPerSeed': 0.1,
                      'impactMax': 3.0,
                      'maxPtScattering': 10.0,
                      'deltaRMin': 1.0,
                      'deltaRMax': 60.0}
    sequence.run(time_path, default_params)
