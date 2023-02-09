import argparse
import optimize_optuna
import get_parameter_pngs
import get_score_png
import get_best_trial
import get_trial_pngs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('--path', nargs=3)
    parser.add_argument('--label', nargs=3)
    args = parser.parse_args()

    if args.command == 'optimize_optuna':
        optimize_optuna.optimize()

    if args.command == 'get_best_trial':
        # args.file: filestring of the .db file
        get_best_trial.get_best_trial(args.path)

    if args.command == 'get_study_pngs':
        # args.path: root file list path
        # args.pathh: study.db path
        get_parameter_pngs.get_parameter_pngs(args.path, args.pathh)
        get_score_png.get_score_png(args.pathh)

    if args.command == 'get_efficiency_pngs_separate':
        # args.path: list of paths
        get_trial_pngs.get_efficiency_pngs_separate(args.path)

    if args.command == 'get_efficiency_pngs_combined':
        get_trial_pngs.get_efficiency_pngs_combined(args.path, args.label)

    if args.command == 'get_total_pngs':
        get_trial_pngs.get_total_pngs(args.path)

    if args.command == 'get_total_pngs_multiple':
        get_trial_pngs.get_total_pngs_multiple(args.path, args.label)

if __name__ == "__main__":
    main()
