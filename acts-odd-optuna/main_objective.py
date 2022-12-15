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
import datetime
import json
import logging
import matplotlib
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import optuna
import os
import pandas as pd
import pathlib
import pprint
import random
import subprocess
import sys
import time
import uproot
import warnings
import yaml

curDir = Path(os.getcwd())
srcDir = curDir


def run_trial(params, values):
    if len(params) != len(values):
        raise Exception("Length of Params must equal values")

    sequence_script = srcDir / "main_sequence.py"
    ret = ["python"]
    ret.append(sequence_script)

    i = 0
    for param in params:
        arg = "--sf_" + values[i] + "=" + str(param)
        ret.append(arg)
        i += 1

    subprocess.call(ret)


class Objective:
    def __init__(self, k_dup, k_time):
        self.res = {
            "eff": [],
            "fakerate": [],
            "duplicaterate": [],
            "runtime": [],
        }

        self.k_dup = k_dup
        self.k_time = k_time

    def __call__(self, trial):
        params = []

        maxSeedsPerSpM = trial.suggest_int("maxSeedsPerSpM", 0, 10)
        params.append(maxSeedsPerSpM)
        cotThetaMax = trial.suggest_float("cotThetaMax", 5.0, 10.0)
        params.append(cotThetaMax)
        sigmaScattering = trial.suggest_float("sigmaScattering", 0.2, 50)
        params.append(sigmaScattering)
        radLengthPerSeed = trial.suggest_float("radLengthPerSeed", 0.001, 0.1)
        params.append(radLengthPerSeed)
        impactMax = trial.suggest_float("impactMax", 0.1, 25)
        params.append(impactMax)
        maxPtScattering = trial.suggest_float("maxPtScattering", 1, 50)
        params.append(maxPtScattering)
        deltaRMin = trial.suggest_float("deltaRMin", 0.25, 30)
        params.append(deltaRMin)
        deltaRMax = trial.suggest_float("deltaRMax", 50, 300)
        params.append(deltaRMax)
        keys = [
            "maxSeedsPerSpM",
            "cotThetaMax",
            "sigmaScattering",
            "radLengthPerSeed",
            "impactMax",
            "maxPtScattering",
            "deltaRMin",
            "deltaRMax",
        ]
        
        run_trial(params, keys)
        outputfile = curDir / "performance_ckf.root"
        rootFile = uproot.open(outputfile)
        self.res["eff"].append(rootFile["eff_particles"].member("fElements")[0])
        self.res["fakerate"].append(rootFile["fakerate_tracks"].member("fElements")[0])
        self.res["duplicaterate"].append(
            rootFile["duplicaterate_tracks"].member("fElements")[0]
        )

        timingfile = curDir / "timing.tsv"
        timing = pd.read_csv(timingfile, sep="\t")
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
        self.res["runtime"].append(time_ckf + time_seeding)

        efficiency = self.res["eff"][-1]
        penalty = (
            self.res["fakerate"][-1]
            + self.res["duplicaterate"][-1] / self.k_dup
            + self.res["runtime"][-1] / self.k_time
        )

        return efficiency - penalty
