import os
import pandas
import uproot
import sequence
import numpy
import json

class Objective:
    def __init__(self, output_path):
        self.k_dup = 5
        self.k_time = 5
        self.output_path = output_path

    def __call__(self, trial):
        # Run the trial, return its score.       
        maxSeedsPerSpM = trial.suggest_int("maxSeedsPerSpM", 0, 10)
        cotThetaMax = trial.suggest_float("cotThetaMax", 5.0, 10.0)
        sigmaScattering = trial.suggest_float("sigmaScattering", 0.2, 50)
        radLengthPerSeed = trial.suggest_float("radLengthPerSeed", 0.001, 0.1)
        impactMax = trial.suggest_float("impactMax", 0.1, 25)
        maxPtScattering = trial.suggest_float("maxPtScattering", 1, 50)
        deltaRMin = trial.suggest_float("deltaRMin", 0.25, 30)
        deltaRMax = trial.suggest_float("deltaRMax", 50, 300)

        trial_path = self.output_path / ('trial_' + str(trial.number))
        trial_path.mkdir()
        root_path = trial_path / "performance_ckf.root"
        timing_path = trial_path / 'timing.tsv'
        
        sequence.run(trial_path,
                     maxSeedsPerSpM,
                     cotThetaMax,
                     sigmaScattering,
                     radLengthPerSeed,
                     impactMax,
                     maxPtScattering,
                     deltaRMin,
                     deltaRMax)

        # We need to delete the trackstates_ckf.root and tracksummary_ckf.root files
        # after the CKFPerformanceWriter is done making performance_ckf.root, because
        # those two files are about 4 GB on average, which is too big to store for my setup.
        

        # should probably move this somewhere else.
        root_file_list_path = self.output_path / 'root_file_list.json'
        if not root_file_list_path.exists():
            root_file_list = [str(root_path)]
            with open(root_file_list_path, 'w') as root_file_list_file:
                json.dump(root_file_list, root_file_list_file)
            
        else:
            with open(root_file_list_path, 'r+') as root_file_list_file:
                root_file_list = json.load(root_file_list_file)
                
                # Because we're reading and replacing this file, we need to
                # seek and truncate. Replace this with a better function.
                
                root_file_list_file.seek(0)
                root_file_list.append(str(root_path))
                json.dump(root_file_list, root_file_list_file)
                root_file_list_file.truncate()
        # should probably move this somewhere else
        
        root_dict = uproot.open(root_path)
        cur_eff_particles = root_dict["eff_particles"].member("fElements")[0]
        cur_fakerate_tracks = root_dict["fakerate_tracks"].member("fElements")[0]
        cur_duplicaterate_tracks = root_dict["duplicaterate_tracks"].member("fElements")[0]
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

        efficiency = cur_eff_particles
        penalty = (cur_fakerate_tracks + cur_duplicaterate_tracks / self.k_dup + cur_runtime / self.k_time)
        score = efficiency - penalty

        return score
