from functools import reduce
from pathlib import Path

from hypothesis import event, given
from hypothesis import strategies as st

from src.io_handler import to_stdout
from src.record import Record
from src.tournament import Tournament

path = Path("data/sample-input.txt")


def givenInput() -> str:
    content = ""
    with open("data/sample-input.txt", 'r') as rf:
        for line in rf:
            content += line
    return content


def expectedOutput() -> str:
    content = ""
    with open("data/expected-output.txt", 'r') as rf:
        for line in rf:
            content += line
    return content


def test_sample_data() -> None:
    """whether the solution for the sample input matches output"""
    epl = Tournament.readInput(path)
    epl.calibrateRankings()
    output: str = to_stdout(epl.ranking_list)
    expected = expectedOutput()
    assert output == expected


@given(
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=0, max_value=100)
)
def test_rules(wins: int, draws: int, losses: int) -> None:
    """
    whether points tally should work according to the rules
    """
    obj = Record(wins, draws, losses)
    print(obj)
    assert obj.points == (3*wins) + draws

    # points tally cannot exceed maximum collectable points
    assert obj.points <= 3*obj.matches

    event(
        """
        ({}, {}, {}) (wins, draws, losses) results {} points (max {})
        """.format(wins, draws, losses, obj.points, 3*obj.matches))


def test_max_cumulative_points() -> None:
    """
    cumulative point tally of all teams should be lesser than
    or equal to thrice the total matches played
    """
    obj = Tournament.readInput(path)
    obj.calibrateRankings()
    result = reduce(lambda x, y: x+y, [i.points for i in obj.ranking_list])
    assert result <= 3*(obj.played)
