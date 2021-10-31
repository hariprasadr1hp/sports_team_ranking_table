"""
Testing current model against another ranking table
"""

from typing import List
from src.tournament import Ranking, Tournament


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


def test_epl_ranking_idempotency(epl: Tournament) -> None:
    old_list = epl.ranking_list

    epl.calibrateRankings()
    new_list = epl.ranking_list

    epl.calibrateRankings()
    epl.calibrateRankings()
    newer_list = epl.ranking_list

    assert newer_list == new_list == old_list
