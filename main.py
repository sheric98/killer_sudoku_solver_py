import argparse

from src.solver_executor import solve_from_json
from src.output_board import display_board


parser = argparse.ArgumentParser()
parser.add_argument('--groups_file', required=True)


def run(groups_file):
    results = solve_from_json(groups_file)

    if not results:
        print('Could not find any solutions')
    elif len(results) > 1:
        print(f'Found {len(results)} solutions')
        print('Here is one:')
        display_board(results[0])
    else:
        print('Solution:')
        display_board(results[0])


if __name__ == '__main__':
    args = parser.parse_args()

    run(args.groups_file)
