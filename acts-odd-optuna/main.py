import datetime
import json
import logging
import optuna
import os
import sys
import objective
import pathlib

def main():
    n_trials = 2
    initial_param_dict = {
        "maxSeedsPerSpM": 1,
        "cotThetaMax": 7.40627,
        "sigmaScattering": 50,
        "radLengthPerSeed": 0.1,
        "impactMax": 3.0,
        "maxPtScattering": 10.0,
        "deltaRMin": 1.0,
        "deltaRMax": 60.0
    }

    output_path = pathlib.Path.cwd() / datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    output_log_path = output_path / 'log.txt'
    study_name = 'study'
    study_path = output_path / (study_name + '.db')
    
    objective_instance = objective.Objective(output_path)
    logger = optuna.logging.get_logger("optuna")
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.addHandler(logging.FileHandler(str(output_log_path)))
    logger.info('This Study will save files in ' + str(output_path))
    score_direction = 'maximize'
    study = optuna.create_study(
        study_name = study_name,
        storage = "sqlite:///{}".format(study_path),
        direction = score_direction,
        load_if_exists = True,
    )
    
    study.enqueue_trial(initial_param_dict)

    logger.info('Calling optimize.')
    study.optimize(objective_instance, n_trials = n_trials)
    logger.info('optimize finished.')

if __name__ == "__main__":
    main()
