import random
from typing import List

import pytest
from hypothesis import event, given
from hypothesis import strategies as st

from src.record import Record
from src.team import Team
from src.tournament import Ranking, Tournament


@given(
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
)
def test_model_same_points(a, b, c, d, e, f):
    # create 6 teams with random records
    names = [
        'alpha', 'beta', 'gamma', 'theta', 'iota',
        'zeta', 'epsilon', 'upsilon', 'psi', 'chi', 'xi'
    ]

    # create 6 teams with random records
    A = Team(random.choice(names), Record(*a))
    B = Team(random.choice(names), Record(*b))
    C = Team(random.choice(names), Record(*c))
    D = Team(random.choice(names), Record(*d))
    E = Team(random.choice(names), Record(*e))
    F = Team(random.choice(names), Record(*f))

    # instatiate a tournament with these six teams
    # and calibrate their rankings
    tmt = Tournament()
    tmt.teams = {team.name: team for team in [A, B, C, D, E, F]}
    tmt.calibrateRankings()

    # when two teams score the same amount of points,
    # they should share the same rank
    points = [i.points for i in tmt.ranking_list]
    same_points = set([i for i in points if points.count(i) > 1])

    all_similar_points: List[List[Ranking]] = []

    while len(same_points) > 0:
        temp = same_points.pop()
        similar_points = [i for i in tmt.ranking_list if i.points == temp]
        all_similar_points.append(similar_points)

    for i in all_similar_points:
        rank = i[0].rank
        for j in i:
            assert j.rank == rank
        event("'{}' are at ({}) points, hence share the same rank ({})".format(
            [k.name for k in i], i[0].points, rank
        ))


@given(
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
)
def test_model_same_rank(a, b, c, d, e, f):
    # create 6 teams with random records
    names = [
        'alpha', 'beta', 'gamma', 'theta', 'iota',
        'zeta', 'epsilon', 'upsilon', 'psi', 'chi', 'xi'
    ]

    # create 6 teams with random records
    A = Team(random.choice(names), Record(*a))
    B = Team(random.choice(names), Record(*b))
    C = Team(random.choice(names), Record(*c))
    D = Team(random.choice(names), Record(*d))
    E = Team(random.choice(names), Record(*e))
    F = Team(random.choice(names), Record(*f))

    # instatiate a tournament with these six teams
    # and calibrate their rankings
    tmt = Tournament()
    tmt.teams = {team.name: team for team in [A, B, C, D, E, F]}
    tmt.calibrateRankings()

    # when two teams score the same rank,
    # they should have scored same points
    rankings = [i.rank for i in tmt.ranking_list]
    same_rankings = set([i for i in rankings if rankings.count(i) > 1])

    all_similar_rankings: List[List[Ranking]] = []

    while len(same_rankings) > 0:
        temp = same_rankings.pop()
        similar_rankings = [i for i in tmt.ranking_list if i.rank == temp]
        all_similar_rankings.append(similar_rankings)

    for i in all_similar_rankings:
        point = i[0].points
        for j in i:
            assert j.points == point
        event("'{}' have same rank({}), because they share same points ({})".format(
            [k.name for k in i], i[0].rank, point
        ))


@given(
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
    st.lists(st.integers(min_value=0, max_value=100), min_size=3, max_size=3),
)
def test_alphabetical_order(a, b, c, d, e, f):
    names = [
        'alpha', 'beta', 'gamma', 'theta', 'iota',
        'zeta', 'epsilon', 'upsilon', 'psi', 'chi', 'xi'
    ]

    # create 6 teams with random records
    A = Team(random.choice(names), Record(*a))
    B = Team(random.choice(names), Record(*b))
    C = Team(random.choice(names), Record(*c))
    D = Team(random.choice(names), Record(*d))
    E = Team(random.choice(names), Record(*e))
    F = Team(random.choice(names), Record(*f))

    # instatiate a tournament with these six teams
    # and calibrate their rankings
    tmt = Tournament()
    tmt.teams = {team.name: team for team in [A, B, C, D, E, F]}
    tmt.calibrateRankings()

    # when two teams score the same rank,
    # they should have scored same points
    rankings = [i.rank for i in tmt.ranking_list]
    same_rankings = set([i for i in rankings if rankings.count(i) > 1])

    all_similar_rankings: List[List[Ranking]] = []

    while len(same_rankings) > 0:
        temp = same_rankings.pop()
        similar_rankings = [i for i in tmt.ranking_list if i.rank == temp]
        all_similar_rankings.append(similar_rankings)

    for i in all_similar_rankings:
        point = i[0].points
        for j in i:
            assert j.points == point
        event("More than one team have the same rank({}) due to same points ({}). The printing order is, '{}'".format(
            i[0].rank, point, [k.name for k in i]
        ))
