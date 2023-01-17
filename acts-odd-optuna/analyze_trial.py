import optuna

def get_best_trial_params(dir_string):
    # dir_string: String of the relative path to the simulation directory, e.g. 2023-01-13-00-07-47
    study_file_path = 'sqlite:///{}/study.db'.format(dir_string)
    study_name = 'study'
    study = optuna.load_study(storage = study_file_path,
                              study_name = study_name)
    print(study.best_trial)
