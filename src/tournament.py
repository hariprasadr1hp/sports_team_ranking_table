import os
import re
import sys
from dataclasses import InitVar, dataclass, field
from typing import Dict, List, NewType, Pattern

from src.io_handler import IOHandler, ReadWriteOper
from src.match import Match
from src.record import Record
from src.team import Team

# Path = NewType('Path', str)

class Path(str):
    def __init__(self, path: str) -> None:
        super().__init__()
        try:
            self.path = self.validatePath(path)
        except FileNotFoundError:
            print("Path '{path}' not found".format(path=path))
            sys.exit()
    
    @staticmethod
    def validatePath(path):
        if os.path.exists(path):
            return path
        raise FileNotFoundError

@dataclass
class Tournament:
    fname: InitVar[Path] = field(repr=False)
    name: str = "Bundesliga"
    teams: Dict[str, Team] = field(init=False, default_factory=dict)
    matches: List[Match] = field(init=False, default_factory=list)

    @property
    def played(self):
        """ total matches played """
        return len(self.matches)

    @staticmethod
    def parseLine(line: str):
        pattern = r'\s*(.+)\s+(\d)\s*,\s*(.+)\s+(\d)\s*'
        regex: Pattern[str] = re.compile(pattern=pattern)
        matches = regex.findall(line)[0]
        return matches

    def writeOutput(self):
        table = sorted(self.teams.values(), reverse=True)
        i: int = 1
        for i, team in enumerate(table, start=1):
            print("{}. {}, {} pts".format(i, team.name, team.record.points))

    def readInput(self) -> None:
        with open(self.fname, 'r') as rf:
            for line in rf:
                match = Match.fromString(line)
                self.matches.append(match)

                if (name := match.teamA.name) not in self.teams:
                    self.teams[name] = Team(name)
                self.teams[name].record.add_result(match.teamA.result)

                if (name := match.teamB.name) not in self.teams:
                    self.teams[name] = Team(name)
                self.teams[name].record.add_result(match.teamB.result)

        self.writeOutput()

    def __post_init__(self, fname: Path) -> None:
        self.fname = fname
        self.readInput()

        # if os.path.exists(fname):
        #     self.fname = fname
        #     self.readInput()
        # else:
        #     raise FileNotFoundError("Input file '{}' not found".format(fname))
