import argparse
import optimize_optuna
import get_parameter_pngs
import get_score_png
import get_best_trial
import performance_ckf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('--path')
    parser.add_argument('--pathh')
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

    if args.command == 'get_trial_pngs':
        # args.path: path to performance_ckf.root
        performance_ckf.get_efficiency_pngs(args.path)

if __name__ == "__main__":
    main()
