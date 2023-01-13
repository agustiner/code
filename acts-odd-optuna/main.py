import argparse
import pathlib
import optimize
import analyze_root
import analyze_score
import analyze_trial

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('paramA', nargs = '?')
    args = parser.parse_args()

    if args.command == 'get_best_trial':
        # args.paramA: String of the relative path to the simulation directory, e.g. 2023-01-13-00-07-47
        analyze_trial.get_best_trial_params(args.paramA)

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
