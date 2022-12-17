from optuna.visualization import plot_contour
from optuna.visualization import plot_edf
from optuna.visualization import plot_intermediate_values
from optuna.visualization import plot_optimization_history
from optuna.visualization import plot_parallel_coordinate
from optuna.visualization import plot_param_importances
from optuna.visualization import plot_slice
from pathlib import Path
from typing import Optional, Union
import argparse
import array
import json
import logging
import multiprocessing
import numpy as np
import optuna
import os
import pprint
import random
import sys
import main_objective
curDir = Path(os.getcwd())
srcDir = curDir

def main():
    # Parameters.
    k_dup = 5
    k_time = 5
    n_trials = 3
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

    # Objective function.
    objective = main_objective.Objective(k_dup, k_time)

    # Output files.
    outputDir = Path(curDir)
    outputDir.mkdir(exist_ok=True)

    optuna.logging.get_logger("optuna").addHandler(logging.StreamHandler(sys.stdout))
    study_name = "test_study"
    storage_name = "sqlite:///{}.db".format(study_name)

    study = optuna.create_study(
        study_name=study_name,
        storage="sqlite:///{}.db".format(study_name),
        direction="maximize",
        load_if_exists=True,
    )
    study.enqueue_trial(initial_param_dict)
    
    study.optimize(objective, n_trials = n_trials)

    print("Best Trial until now")
    for key, value in study.best_trial.params.items():
        print(f"{key}: {value}")

    outputDir = Path("OptunaResults")
    outputDir.mkdir(exist_ok=True)

    with open(outputDir / "results.json", "w") as results_file:
        json.dump(study.best_params, results_file)

if __name__ == "__main__":
    main()
