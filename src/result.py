from __future__ import annotations

import enum
import os
import re
from dataclasses import InitVar, dataclass, field
from typing import Callable, Dict, List, NewType, Pattern

Path = NewType('Path', str)


@enum.unique
class Result(enum.Enum):
    LOSS = enum.auto()
    DRAW = enum.auto()
    WIN = enum.auto()


@dataclass(order=True)
class Record:
    sort_points: int = field(init=False, repr=False)
    sort_wins: int = field(init=False, repr=False)
    wins: int = 0
    draws: int = 0
    losses: int = 0

    @property
    def points(self) -> int:
        return self.formula(self.wins, self.draws, self.losses)

    @points.setter
    def points(self) -> int:
        raise Exception("Points cannot be set directly...")

    @property
    def matches(self) -> int:
        return self.wins + self.draws + self.losses

    @property
    def formula(self) -> Callable[[int, int, int], int]:
        return self._formula

    @formula.setter
    def formula(self, value: Callable[[int, int, int], int]) -> None:
        self._formula = value

    def add_result(self, result: Result) -> None:
        if isinstance(result, Result):
            if result == Result.WIN:
                self.wins += 1
            elif result == Result.DRAW:
                self.draws += 1
            elif result == Result.LOSS:
                self.losses += 1
        else:
            raise TypeError("not a valid result type")

    def __post_init__(self) -> None:
        self._formula = lambda wins, draws, losses: (
            3*wins) + (1*draws) + (0*losses)
        self.sort_points = self.points
        self.sort_wins = self.wins


@dataclass(order=True)
class Team:
    """
    The team's name and the account of it's records
    """
    sort_index: Record = field(init=False, repr=False)
    name: str
    record: Record = Record(0, 0, 0)

    def __post_init__(self) -> None:
        self.sort_index = self.record


@dataclass(order=True)
class TeamMatchGoals:
    """
    Goals scored by a single team in the match
    """
    sort_goals: int = field(init=False, repr=False)
    name: str
    goals: int

    def __post_init__(self) -> None:
        self.sort_goals = self.goals
        self.result = Result.DRAW


@dataclass
class Match:
    """
    Performance and Results for both the teams on the matchday
    """
    teamA: TeamMatchGoals
    teamB: TeamMatchGoals

    @classmethod
    def fromString(cls, string: str) -> Match:
        pattern = r'\s*(.+)\s+(\d)\s*,\s*(.+)\s+(\d)\s*'
        regex: Pattern[str] = re.compile(pattern=pattern)
        matches = regex.findall(string)[0]
        teamA = TeamMatchGoals(matches[0], matches[1])
        teamB = TeamMatchGoals(matches[2], matches[3])
        return cls(teamA, teamB)

    def __post_init__(self) -> None:
        if self.teamA.goals > self.teamB.goals:
            self.teamA.result = Result.WIN
            self.teamB.result = Result.LOSS

        elif self.teamA.goals < self.teamB.goals:
            self.teamA.result = Result.LOSS
            self.teamB.result = Result.WIN
        else:
            self.teamA.result = Result.DRAW
            self.teamB.result = Result.DRAW


@dataclass
class Tournament:
    fname: InitVar[Path] = field(repr=False)
    name: str = "Bundesliga"
    # teams: Dict[str, Team] = field(init=False, default_factory=dict)
    teams: Dict[str, Team] = field(init=False, default_factory=dict)
    matches: List[Match] = field(init=False, default_factory=list)

    @property
    def played_matches(self):
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
                    self.teams[name] = Team(name, Record())
                self.teams[name].record.add_result(match.teamA.result)

                if (name := match.teamB.name) not in self.teams:
                    self.teams[name] = Team(name, Record())
                self.teams[name].record.add_result(match.teamB.result)

        self.writeOutput()

    def __post_init__(self, fname: Path) -> None:
        if os.path.exists(fname):
            self.fname = fname
            # self.teams: Dict[str, Team] = {}
            self.readInput()
        else:
            raise FileNotFoundError("Input file '{}' not found".format(fname))
