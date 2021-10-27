from __future__ import annotations

import os
import re
from dataclasses import InitVar, dataclass, field
from typing import (Callable, Dict, List, Literal, NewType, Optional, Pattern, Set,
                    Tuple, TypeVar)

Outcome = Optional[Literal['win', 'draw', 'loss']]
Path = NewType('Path', str)


@dataclass(order=True)
class Record:
    sort_index: int = field(init=False, repr=False)
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
    def formula(self) -> Callable[[int, int, int], int]:
        return self._formula

    @formula.setter
    def formula(self, value: Callable[[int, int, int], int]) -> None:
        self._formula = value

    def add_result(self, result: Outcome) -> None:
        if result in ['win', 'draw', 'loss']:
            self.matches += 1
            if result == 'win':
                self.wins += 1
            elif result == 'draw':
                self.draws += 1
            elif result == 'loss':
                self.losses += 1
        else:
            raise TypeError("not a valid result type")

    def __post_init__(self) -> None:
        self.matches = self.wins + self.draws + self.losses
        self._formula = lambda wins, draws, losses: (
            3*wins) + (1*draws) + (0*losses)
        self.sort_index = self.points


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
    sort_index: int = field(init=False, repr=False)
    name: str
    goals: int
    result: Optional[Outcome] = field(default=None, init=False)

    def __post_init__(self) -> None:
        self.sort_index = self.goals


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
        if self.teamA == self.teamB:
            self.teamA.result = 'draw'
            self.teamB.result = 'draw'

        elif self.teamA > self.teamB:
            self.teamA.result = 'win'
            self.teamB.result = 'loss'

        elif self.teamA < self.teamB:
            self.teamA.result = 'loss'
            self.teamB.result = 'win'


@dataclass
class PointsTable:
    ...


@dataclass
class Tournament:
    fname: InitVar[Path] = field(repr=False)
    name: str = "Bundesliga"
    matches: int = 0

    @staticmethod
    def parseLine(line: str):
        pattern = r'\s*(.+)\s+(\d)\s*,\s*(.+)\s+(\d)\s*'
        regex: Pattern[str] = re.compile(pattern=pattern)
        matches = regex.findall(line)[0]
        return matches

    def readInput(self) -> None:
        with open(self.fname, 'r') as rf:
            for line in rf:
                match = Match.fromString(line)

                if (name := match.teamA.name) not in self.teams:
                    self.teams[name] = Team(name)

                self.teams[name].record.add_result(match.teamA.result)

                if (name := match.teamB.name) not in self.teams:
                    self.teams[name] = Team(name)

                print(match.teamA.result)

                self.teams[name].record.add_result(match.teamB.result)

        print(self.teams)

    def __post_init__(self, fname: Path) -> None:
        if os.path.exists(fname):
            self.fname = fname
            self.teams: Dict[str, Team] = {}
            self.readInput()
        else:
            raise FileNotFoundError("Input file '{}' not found".format(fname))
