import datetime
import logging
import objective
import optuna
import pathlib
import sys
import get_time_dir

def optimize():
    n_trials = 200
    initial_param_dict = {
        'maxSeedsPerSpM': 1,
        'cotThetaMax': 7.40627,
        'sigmaScattering': 5,
        'radLengthPerSeed': 0.1,
        'impactMax': 3.0,
        'maxPtScattering': 10.0,
        'deltaRMin': 1.0,
        'deltaRMax': 60.0
    }

    output_path = get_time_dir.get_time_dir()
    output_log_path = output_path / 'log.txt'
    study_name = 'study'
    study_path = output_path / (study_name + '.db')
    
    objective_instance = objective.Objective(output_path)
    logger = optuna.logging.get_logger('optimize')
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.addHandler(logging.FileHandler(str(output_log_path)))
    logger.info('This Study will save files in ' + str(output_path))
    study = optuna.create_study(
        study_name = study_name,
        storage = "sqlite:///{}".format(study_path),
        direction = 'maximize'
    )
    study.enqueue_trial(initial_param_dict)
    logger.info('Calling optimize.')
    study.optimize(objective_instance, n_trials = n_trials)
    logger.info('Done calling optimize.')
