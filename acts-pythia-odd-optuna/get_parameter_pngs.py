# Review the optimization study's data, make plots, etc.
import optuna
from matplotlib import pyplot

def get_study(study_path):
    study_name = 'study'
    storage_string = 'sqlite:///{}'.format(study_path)
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

def get_study_figure(points, xaxis_string, yaxis_string):
    pyplot.rcParams['font.family'] = 'Times New Roman'
    figure = pyplot.figure(figsize = (6, 3))
    ax1 = figure.add_subplot()
    ax1.plot(points)
    ax1.set_title(yaxis_string)
    ax1.set_xlabel(xaxis_string)
    ax1.set_ylabel(yaxis_string)
    for ax in figure.axes:
        ax.get_lines()[0].set_color("black")

    return figure

def get_parameter_pngs(root_file_list_path, study_path):
    parameter_list = ['cotThetaMax', 'deltaRMax', 'deltaRMin', 'impactMax', 'maxPtScattering', 'maxSeedsPerSpM', 'radLengthPerSeed', 'sigmaScattering']
    study = get_study(study_path)
    for parameter in parameter_list:
        points = get_study_points(parameter, study)
        fig = get_study_figure(points, "Trial", parameter)
        pyplot.savefig(parameter + '.png', bbox_inches='tight', dpi = 200)

