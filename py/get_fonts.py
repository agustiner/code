from matplotlib import pyplot
import matplotlib.font_manager as fm
font_names = [f.name for f in fm.fontManager.ttflist]
font_names.sort()
print(font_names)
