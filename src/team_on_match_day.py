from dataclasses import dataclass, field

from src.result import Result


@dataclass(order=True)
class TeamOnMatchDay:
    """
    Goals and game result of one team on the matchday
    """
    sort_goals: int = field(init=False, repr=False)
    name: str
    goals: int

    def __post_init__(self) -> None:
        self.sort_goals = self.goals
        self.result = Result.DRAW
