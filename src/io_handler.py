import enum
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import List

from src.tournament import Ranking


def to_stdout(ranking_list: List[Ranking]) -> str:
    """returns string, ready to be printed"""
    content = io.StringIO()
    sys.stdout.flush()

    with redirect_stdout(content):
        for team in ranking_list:
            suffix = "pt" if team.points == 1 else "pts"
            sys.stdout.write("{}. {}, {} {}\n".format(
                team.rank, team.name, team.points, suffix))

    return content.getvalue()


def to_csv(ranking_list: List[Ranking], path: Path) -> bool:
    """stores the ranking details to a csv file"""
    if path.parent.exists():
        with open(path, 'w') as f:
            for team in ranking_list:
                suffix = "pt" if team.points == 1 else "pts"
                f.write("{}. {}, {} {}\n".format(
                    team.rank, team.name, team.points, suffix))
        return True
    return False


@enum.unique
class IOHandler(enum.Enum):
    NONE = enum.auto()
    STDOUT = enum.auto()
    STDIN = enum.auto()
    CSV = enum.auto()
    SQL = enum.auto()
    PICKLE = enum.auto()
