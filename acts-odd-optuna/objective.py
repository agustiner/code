from pathlib import Path
import os
import pandas
import uproot
import sequence

class Objective:
    def __init__(self):
        self.res = {
            "eff": [],
            "fakerate": [],
            "duplicaterate": [],
            "runtime": [],
        }
        self.k_dup = 5
        self.k_time = 5

    def __call__(self, trial):
        maxSeedsPerSpM = trial.suggest_int("maxSeedsPerSpM", 0, 10)
        cotThetaMax = trial.suggest_float("cotThetaMax", 5.0, 10.0)
        sigmaScattering = trial.suggest_float("sigmaScattering", 0.2, 50)
        radLengthPerSeed = trial.suggest_float("radLengthPerSeed", 0.001, 0.1)
        impactMax = trial.suggest_float("impactMax", 0.1, 25)
        maxPtScattering = trial.suggest_float("maxPtScattering", 1, 50)
        deltaRMin = trial.suggest_float("deltaRMin", 0.25, 30)
        deltaRMax = trial.suggest_float("deltaRMax", 50, 300)
        
        sequence.run(maxSeedsPerSpM,
                     cotThetaMax,
                     sigmaScattering,
                     radLengthPerSeed,
                     impactMax,
                     maxPtScattering,
                     deltaRMin,
                     deltaRMax)

        curDir = Path(os.getcwd())
        outputfile = curDir / "performance_ckf.root"
        rootFile = uproot.open(outputfile)
        self.res["eff"].append(rootFile["eff_particles"].member("fElements")[0])
        self.res["fakerate"].append(rootFile["fakerate_tracks"].member("fElements")[0])
        self.res["duplicaterate"].append(
            rootFile["duplicaterate_tracks"].member("fElements")[0]
        )

        timingfile = curDir / "timing.tsv"
        timing = pandas.read_csv(timingfile, sep="\t")
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
        score = efficiency - penalty

        return score
