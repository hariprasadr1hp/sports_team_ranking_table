from dataclasses import dataclass, field
from typing import Callable

from src.result import Result


@dataclass(order=True)
@dataclass
class Record:
    """
    A counter for the wins, draws and losses
    """
    sort_points: int = field(init=False, repr=False)
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
    def matches(self) -> int:
        return self.wins + self.draws + self.losses

    @property
    def formula(self) -> Callable[[int, int, int], int]:
        return self._formula

    @formula.setter
    def formula(self, value: Callable[[int, int, int], int]) -> None:
        self._formula = value

    def add_result(self, result: Result) -> None:
        if isinstance(result, Result):
            if result == Result.WIN:
                self.wins += 1
            elif result == Result.DRAW:
                self.draws += 1
            elif result == Result.LOSS:
                self.losses += 1
        else:
            raise TypeError("not a valid result type")

    def __eq__(self, other) -> bool:
        w = self.wins == other.wins
        d = self.draws == other.draws
        l = self.losses == other.losses
        return w and d and l

    def __post_init__(self) -> None:
        self._formula = lambda wins, draws, losses: (
            3*wins) + (1*draws) + (0*losses)
        self.sort_points = self.points
