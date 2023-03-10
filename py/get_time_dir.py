import datetime
import pathlib

def get_time_dir():
    output_path = pathlib.Path.cwd() / datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    output_path.mkdir()
    return output_path
