from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, NamedTuple

from src.match import Match
from src.team import Team


class Ranking(NamedTuple):
    rank: int
    name: str
    points: int


@dataclass
class Tournament:
    name: str = "Sports League"
    teams: Dict[str, Team] = field(default_factory=dict)
    matches: List[Match] = field(default_factory=list)
    ranking_list: List[Ranking] = field(
        init=False, repr=False, default_factory=list)

    @classmethod
    def readInput(cls, path: Path, name="Sports League") -> Tournament:
        """
        reading input form a *.txt file and updating matches
        and team records
        """
        matches: List[Match] = []
        teams: Dict[str, Team] = {}
        with open(path, 'r') as rf:
            for line in rf:
                match = Match.fromString(line)
                matches.append(match)

                if (name := match.teamA.name) not in teams:
                    teams[name] = Team(name)
                teams[name].record.add_result(match.teamA.result)

                if (name := match.teamB.name) not in teams:
                    teams[name] = Team(name)
                teams[name].record.add_result(match.teamB.result)

        return cls(name, teams, matches)

    @property
    def played(self) -> int:
        """ total matches played """
        return len(self.matches)

    def calibrateRankings(self) -> None:
        """
        rank simulation from the given team records
        """
        table = sorted(self.teams.values())

        self.ranking_list: List[Ranking] = []

        names: List[str] = [team.name for team in table]
        points: List[int] = [team.record.points for team in table]

        # ranking from the top
        rank: int = 1
        higher_rank: int = 1
        higher_point: int = max(points)
        count: int = 1
        while len(names) > 0:
            index: int = points.index(max(points))
            name: str = names.pop(index)
            point: int = points.pop(index)

            if point == higher_point:
                rank = higher_rank

            self.ranking_list.append(Ranking(rank, name, point))

            higher_rank = rank
            higher_point = point
            count += 1
            rank = count
