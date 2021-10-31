import argparse
from pathlib import Path
import sys

from src.io_handler import to_stdout
from src.tournament import Tournament


def main():
    epl = Tournament.readInput(path)
    epl.calibrateRankings()
    content: str = to_stdout(epl.ranking_list)
    print(content, end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
            A command-line application that calculates ranking table
            for a sports league."""
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=False,
        metavar='',
        help='a txt file with results of game, one per line'
    )

    args = parser.parse_args()

    try:
        path = Path(args.input)
    except TypeError:
        print("""
            No input file provided!
            try `python main.py --input='{{input-file}}'`""")
        sys.exit()

    if path.exists():
        main()
    else:
        raise FileNotFoundError("Input file '{}' not found".format(path))
