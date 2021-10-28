from pathlib import Path

from src.io_handler import to_stdout, to_csv
from src.tournament import Tournament

path = Path("data/sample-input.txt")
epl = Tournament(path)

ierr = to_stdout(epl.table)
ierr = to_csv(epl.table, path=Path("data/cees.csv"))
