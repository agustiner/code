# Review the optimization study's data, make plots, etc.
import optuna
from matplotlib import pyplot

def get_study():
    study_name = 'study'
    study_path = '/home/user1/code/acts-odd-optuna/2022-12-21-19-20-29/{}.db'.format(study_name)
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

def get_study_plots():
    parameter_list = ['cotThetaMax', 'deltaRMax', 'deltaRMin', 'impactMax', 'maxPtScattering', 'maxSeedsPerSpM', 'radLengthPerSeed', 'sigmaScattering']
    study = get_study()
    for parameter in parameter_list:
        points = get_study_points(parameter, study)
        fig = get_study_figure(points, "Trial", parameter)
        pyplot.savefig(parameter + '.png', bbox_inches='tight', dpi = 200)

