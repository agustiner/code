import optuna

def get_study(path):
    study_file_path = 'sqlite:///{}'.format(str(path))
    study_name = 'study'
    study = optuna.load_study(storage = study_file_path,
                              study_name = study_name)

    return study

def get_best_trial(path):
    # path of the .db file
    study = get_study(path / 'study.db')
    best_trial = study.best_trial

    print('Best trial:')
    print(best_trial)

    return best_trial.number
