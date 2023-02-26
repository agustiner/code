from matplotlib import pyplot
from matplotlib.ticker import StrMethodFormatter

def get_study_figure(points, x_str, y_str, title_str):
    pyplot.rcParams['font.family'] = 'Times New Roman'
    figure = pyplot.figure(figsize = (4, 3))
    ax1 = figure.add_subplot()
    ax1.plot(points)
    ax1.set_title(title_str)
    ax1.set_xlabel(x_str)
    ax1.set_ylabel(y_str)
    # Always format the figure with two decimals. This makes it easy
    # to combine multiple figures into a grid, because they will have
    # exactly the same proportions, assuming the labels don't overflow.
    # ax1.yaxis.set_major_formatter(StrMethodFormatter('{x:.2f}'))
    for ax in figure.axes:
        ax.get_lines()[0].set_color("black")

    figure.tight_layout()
    return figure

def get_grid(nx, ny, points, xlabels, titles, path):
    figure, axes = pyplot.subplots(nrows=nx, ncols=ny, constrained_layout=True)

    for i, a in enumerate(axes.flat):
        a.set_xlabel(xlabels[i])
        a.set_title(titles[i])
        a.plot(points[i])
        a.get_lines()[0].set_color("black")

    figure.tight_layout()
    pyplot.savefig(path / 'grid.png', dpi = 200)
