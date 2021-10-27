from dataclasses import dataclass, field

from src.result import Result


@dataclass(order=True)
class TeamOnMatchDay:
    """
    Goals scored by a single team in the match
    """
    sort_goals: int = field(init=False, repr=False)
    name: str
    goals: int

    def __post_init__(self) -> None:
        self.sort_goals = self.goals
        self.result = Result.DRAW
