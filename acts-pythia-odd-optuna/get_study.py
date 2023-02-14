import optuna

def get_study(path):
    study_file_path = 'sqlite:///{}'.format(path)
    study_name = 'study'
    study = optuna.load_study(storage = study_file_path,
                              study_name = study_name)

    return study

def get_best_trial(path):
    # path of the .db file
    study = get_study(path)
    print(study.best_trial)
