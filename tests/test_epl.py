"""
Testing current model against another ranking table
"""

from typing import List

import pytest

from src.record import Record
from src.team import Team
from src.tournament import Ranking, Tournament


@pytest.fixture
def epl() -> Tournament:
    """
    creating a mock fixture and check
    whether the results are reproducible
    """
    tmt = Tournament()
    tmt.teams['arsenal'] = Team('arsenal', Record(5, 2, 3))
    tmt.teams['chelsea'] = Team('chelsea', Record(8, 1, 1))
    tmt.teams['manutd'] = Team('manutd', Record(5, 2, 3))
    tmt.teams['mancity'] = Team('mancity', Record(6, 2, 2))
    tmt.teams['spurs'] = Team('spurs', Record(5, 0, 5))
    tmt.teams['liverpool'] = Team('liverpool', Record(6, 4, 0))
    tmt.calibrateRankings()
    return tmt


def test_epl_same_points(epl: Tournament) -> None:
    """
    when two teams score the same amount of points,
    they should share the same rank
    """
    points = [i.points for i in epl.ranking_list]
    same_points = set([i for i in points if points.count(i) > 1])

    all_similar_points: List[List[Ranking]] = []

    while len(same_points) > 0:
        temp = same_points.pop()
        similar_points = [i for i in epl.ranking_list if i.points == temp]
        all_similar_points.append(similar_points)

    for i in all_similar_points:
        rank = i[0].rank
        for j in i:
            assert j.rank == rank


def test_epl_same_rankings(epl: Tournament) -> None:
    """
    when two teams score the same amount of points,
    they should share the same rank
    """
    rankings = [i.rank for i in epl.ranking_list]
    same_rankings = set([i for i in rankings if rankings.count(i) > 1])

    all_similar_rankings: List[List[Ranking]] = []

    while len(same_rankings) > 0:
        temp = same_rankings.pop()
        similar_rankings = [i for i in epl.ranking_list if i.rank == temp]
        all_similar_rankings.append(similar_rankings)

    for i in all_similar_rankings:
        point = i[0].points
        for j in i:
            assert j.points == point
