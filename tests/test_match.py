from hypothesis import event, given
from hypothesis import strategies as st

from src.match import Match
from src.record import Record
from src.team import Team
from src.team_on_match_day import TeamOnMatchDay


@given(
    st.integers(min_value=0, max_value=20),
    st.integers(min_value=0, max_value=20),
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=0, max_value=100),
)
def test_match_results(score1, score2, w1, d1, l1, w2, d2, l2):
    # match results are properly updated
    Alpha = Team("Alpha", Record(w1, d1, l1))
    Beta = Team("Beta", Record(w2, d2, l2))

    A = TeamOnMatchDay(Alpha.name, score1)
    B = TeamOnMatchDay(Beta.name, score2)
    match = Match(A, B)
    Alpha.record.add_result(match.teamA.result)
    Beta.record.add_result(match.teamB.result)

    if match.teamA.goals > match.teamB.goals:
        assert Alpha.record == Record(w1+1, d1, l1)
        assert Beta.record == Record(w2, d2, l2+1)

    elif match.teamA.goals < match.teamB.goals:
        assert Alpha.record == Record(w1, d1, l1+1)
        assert Beta.record == Record(w2+1, d2, l2)

    else:
        assert Alpha.record == Record(w1, d1+1, l1)
        assert Beta.record == Record(w2, d2+1, l2)

    event("A({}) vs B({}) ==> A: {} --- B: {}".format(
        score1, score2, match.teamA.result, match.teamB.result
    ))
