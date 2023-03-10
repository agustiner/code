# Review the optimization study's data, make plots, etc.
import os
import optuna
import get_figure
from matplotlib import pyplot

# path to folder containing study.db
def get_study(study_dirpath):
    study_name = 'study'
    storage_string = 'sqlite:///{}'.format(str(study_dirpath / 'study.db'))
    study = optuna.load_study(study_name = study_name, storage = storage_string)
    return study

def get_study_points(parameter, study):
    # parameter string
    # study Study
    # trial int
    points = list()
    
    for t in study.trials:
        point = t.params[parameter]
        points.append(point)

    return points

def get_study_scores(study):
    # input: Study
    # output: list
    score_list = list()
    
    for t in study.trials:
        score_list.append(t.value)

    return score_list

def get_parameter_per_trial(study_path):
    parameter_list = ['cotThetaMax', 'deltaRMax', 'deltaRMin', 'impactMax', 'maxPtScattering', 'maxSeedsPerSpM', 'radLengthPerSeed', 'sigmaScattering']
    study = get_study(study_path)
    
    for parameter in parameter_list:
        points = get_study_points(parameter, study)
        fig = get_figure.get_study_figure(points, "Trial", '', parameter)
        outpath = study_path / 'parameter_per_trial'        
        if (outpath.exists() == False):
            os.mkdir(outpath)

        pyplot.savefig(outpath / (parameter + '.png'), dpi = 200)

    path = study_path / 'parameter_per_trial'
    points = [get_study_points(parameter, study) for parameter in parameter_list]
    xlabels = ['Trial' for i in range(len(parameter_list))]
    get_figure.get_grid(3, 2, points, xlabels, parameter_list, path)


def get_score_png(path):
    study = get_study(path)
    points = get_study_scores(study)
    fig = get_figure.get_study_figure(points, 'Trial', '', 'Score')
    pyplot.savefig(path / 'score.png', dpi = 200)
