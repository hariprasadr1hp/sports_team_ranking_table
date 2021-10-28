import re
from dataclasses import InitVar, dataclass, field
from pathlib import Path
from typing import Dict, List, Pattern

from src.match import Match
from src.team import Team


@dataclass
class Tournament:
    file: InitVar[Path] = field(repr=False)
    name: str = "Sports League"
    teams: Dict[str, Team] = field(init=False, default_factory=dict)
    matches: List[Match] = field(init=False, default_factory=list)
    table: List[Team] = field(init=False, repr=False, default_factory=list)

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

    def readInput(self) -> None:
        with open(self.file, 'r') as rf:
            for line in rf:
                match = Match.fromString(line)
                self.matches.append(match)

                if (name := match.teamA.name) not in self.teams:
                    self.teams[name] = Team(name)
                self.teams[name].record.add_result(match.teamA.result)

                if (name := match.teamB.name) not in self.teams:
                    self.teams[name] = Team(name)
                self.teams[name].record.add_result(match.teamB.result)
        
        self.table = sorted(self.teams.values(), reverse=True)

    def __post_init__(self, file: Path) -> None:
        if file.exists():
            self.file = file
            self.readInput()
        else:
            raise FileNotFoundError("Input file '{}' not found".format(file))
