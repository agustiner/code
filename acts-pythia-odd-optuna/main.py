import argparse
import optimize_optuna
import analyze_trials
import analyze_score
import analyze_get_best_trial
import analyze_performance_ckf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('--file')
    parser.add_argument('--dir')
    args = parser.parse_args()

    if args.command == 'optimize_optuna':
        optimize_optuna.optimize()

    if args.command == 'get_best_trial':
        # args.file: filestring of the .db file
        analyze_get_best_trial.get_best_trial(args.file)

    if args.command == 'get_parameter_pngs':
        # args.dir: String of the relative path to the simulation directory, e.g. 2023-01-13-00-07-47
        analyze_trials.get_parameter_pngs(args.dir)

    if args.command == 'get_score_png':
        # args.dir: String of the relative path to the simulation directory, e.g. 2023-01-13-00-07-47
        analyze_score.get_score_png(args.dir)

    if args.command == 'get_efficiency_pngs':
        # args.file: path to .root file
        analyze_performance_ckf.get_efficiency_pngs(args.file)

if __name__ == "__main__":
    main()
