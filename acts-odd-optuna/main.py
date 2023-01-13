import argparse
import optuna
import pathlib
import optimize
import analyze_root
import analyze_score

def get_best_trial_params():
    study_file_path = 'sqlite:///2023-01-10-14-09-59/study.db'
    study_name = 'study'
    study = optuna.load_study(storage = study_file_path,
                              study_name = study_name)
    print(study.best_trial)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('paramA')
    args = parser.parse_args()

    if args.command == 'get_best_trial':
        get_best_trial_params()

    if args.command == 'analyze_root':
        # args.paramA: String of the relative path to the simulation directory, e.g. 2023-01-13-00-07-47
        analyze_root.analyze_root(args.paramA)

    if args.command == 'optimize':
        optimize.optimize()

    if args.command == 'get_score_plot':
        # args.paramA: String of the relative path to the simulation directory, e.g. 2023-01-13-00-07-47
        analyze_score.get_score_plot(args.paramA)

if __name__ == "__main__":
    main()
