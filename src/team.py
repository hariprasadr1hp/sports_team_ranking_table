from dataclasses import dataclass, field

from src.record import Record


@dataclass(order=True, frozen=True)
class Team:
    """
    Name the team and an account of its records
    
    sorted[name < Record]
    """

    sort_index: Record = field(init=False, repr=False)
    name: str
    record: Record = field(default_factory=Record)

    def __post_init__(self) -> None:
        object.__setattr__(self, 'sort_index', self.record)
