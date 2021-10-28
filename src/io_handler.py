import enum
import io
import sys
from contextlib import redirect_stdout
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List

from src.team import Team

SUCCESS = True
FAILURE = False

def to_stdout(teams: List[Team]) -> bool:
    content = io.StringIO()
    sys.stdout.flush()

    with redirect_stdout(content):
        for i, team in enumerate(teams, start=1):
            sys.stdout.write("{}. {}, {} pts\n".format(
                i, team.name, team.record.points))

    print(content.getvalue(), end="")
    return SUCCESS

def to_csv(teams: List[Team], path: Path) -> bool:
    if path.parent.exists():
        with open(path, 'w') as f:
            for i, team in enumerate(teams, start=1):
                f.write("{}. {}, {} pts\n".format(
                    i, team.name, team.record.points)) 
        return SUCCESS
    return FAILURE
    


@enum.unique
class IOHandler(enum.Enum):
    NONE = enum.auto()
    STDOUT = enum.auto()
    STDIN = enum.auto()
    CSV = enum.auto()
    SQL = enum.auto()
    PICKLE = enum.auto()

