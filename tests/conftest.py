import pytest

from src.record import Record
from src.team import Team
from src.tournament import Tournament


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
