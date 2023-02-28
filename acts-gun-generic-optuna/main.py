import argparse
import pathlib
import optimize
import analyze_trials
import analyze_score
import analyze_get_best_trial
import analyze_performance_ckf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('paramA', nargs = '?')
    args = parser.parse_args()

    if args.command == 'optimize':
        optimize.optimize()

    if args.command == 'get_best_trial':
        # args.paramA: filestring of the .db file
        analyze_get_best_trial.get_best_trial(args.paramA)

    if args.command == 'get_parameter_pngs':
        # args.paramA: String of the relative path to the simulation directory, e.g. 2023-01-13-00-07-47
        analyze_trials.get_parameter_pngs(args.paramA)

    if args.command == 'get_score_png':
        # args.paramA: String of the relative path to the simulation directory, e.g. 2023-01-13-00-07-47
        analyze_score.get_score_png(args.paramA)

    if args.command == 'get_efficiency_pngs':
        # paramA: path to .root file
        analyze_performance_ckf.get_efficiency_pngs(args.paramA)

if __name__ == "__main__":
    main()
