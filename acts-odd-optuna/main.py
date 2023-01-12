import argparse
import optuna
import pathlib

def get_best_trial_params():
    study_file_path = 'sqlite:///2023-01-10-14-09-59/study.db'
    study_name = 'study'
    study = optuna.load_study(storage = study_file_path,
                              study_name = study_name)
    print(study.best_trial)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command') 
    args = parser.parse_args()

    if args.command == 'getbesttrial':
        get_best_trial_params()

    if args.command == 'analyze_root':
        

if __name__ == "__main__":
    main()
