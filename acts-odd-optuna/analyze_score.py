# Make a plot of just the Study's score.
import optuna
from matplotlib import pyplot

def get_study():
    study_name = 'study'
    study_path = '/home/user1/code/acts-odd-optuna/2022-12-21-19-20-29/{}.db'.format(study_name)
    storage_string = 'sqlite:///{}'.format(study_path)
    study = optuna.load_study(study_name = study_name, storage = storage_string)

    return study

def get_study_scores(study):
    # input: Study
    # output: list
    score_list = list()
    
    for t in study.trials:
        score_list.append(t.value)

    return score_list

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

def get_score_plot():
    study = get_study()
    points = get_study_scores(study)
    fig = get_study_figure(points, 'Trial', 'Score')
    pyplot.savefig('score.png', bbox_inches='tight', dpi = 200)

get_score_plot()
