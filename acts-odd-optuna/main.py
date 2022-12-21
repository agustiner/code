from pathlib import Path
import json
import logging
import optuna
import os
import sys
import objective

def main():
    n_trials = 1
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
    score_direction = 'maximize'

    objective_instance = objective.Objective()

    curDir = Path(os.getcwd())
    outputDir = Path(curDir)
    outputDir.mkdir(exist_ok=True)

    logger = optuna.logging.get_logger("optuna")
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.addHandler(logging.FileHandler("./log.txt"))
    
    study_name = "study"
    study = optuna.create_study(
        study_name = study_name,
        storage = "sqlite:///{}.db".format(study_name),
        direction = score_direction,
        load_if_exists = True,
    )
    study.enqueue_trial(initial_param_dict)
    study.optimize(objective_instance, n_trials = n_trials)

    for key, value in study.best_trial.params.items():
        print(f"Best {key}: {value}")

    with open("best_params.json", "w") as results_file:
        json.dump(study.best_params, results_file)

if __name__ == "__main__":
    main()
