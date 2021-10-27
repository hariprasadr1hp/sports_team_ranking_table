from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Pattern

from src.result import Result
from src.team_on_match_day import TeamOnMatchDay


@dataclass
class Match:
    """
    Performance and Results for both the teams on the matchday
    """
    teamA: TeamOnMatchDay
    teamB: TeamOnMatchDay

    @classmethod
    def fromString(cls, string: str) -> Match:
        pattern = r'\s*(.+)\s+(\d)\s*,\s*(.+)\s+(\d)\s*'
        regex: Pattern[str] = re.compile(pattern=pattern)
        matches = regex.findall(string)[0]
        teamA = TeamOnMatchDay(name=matches[0], goals=matches[1])
        teamB = TeamOnMatchDay(name=matches[2], goals=matches[3])
        return cls(teamA, teamB)

    def updateMatchResults(self):
        if self.teamA.goals > self.teamB.goals:
            self.teamA.result = Result.WIN
            self.teamB.result = Result.LOSS

        elif self.teamA.goals < self.teamB.goals:
            self.teamA.result = Result.LOSS
            self.teamB.result = Result.WIN
        else:
            self.teamA.result = Result.DRAW
            self.teamB.result = Result.DRAW

    def __post_init__(self) -> None:
        self.updateMatchResults()
