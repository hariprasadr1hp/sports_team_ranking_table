from src.record import Record
from src.result import Result


def test_results_update() -> None:
    """
    basic testing to validate if the results are 
    updated correctly
    """
    a = Record(0, 0, 0)
    a.add_result(Result.WIN)
    assert a == Record(1, 0, 0)
    a.add_result(Result.DRAW)
    assert a == Record(1, 1, 0)
    a.add_result(Result.LOSS)
    assert a == Record(1, 1, 1)
