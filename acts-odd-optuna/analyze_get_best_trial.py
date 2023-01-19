import optuna

def get_best_trial(filestring):
    # filestring of the .db file
    study_file_path = 'sqlite:///{}'.format(filestring)
    study_name = 'test_study'
    study = optuna.load_study(storage = study_file_path,
                              study_name = study_name)
    print(study.best_trial)
