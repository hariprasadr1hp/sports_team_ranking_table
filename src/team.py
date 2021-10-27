from dataclasses import dataclass, field

from src.record import Record


@dataclass(order=True)
class Team:
    """
    The team's name and the account of it's records
    """
    sort_index: Record = field(init=False, repr=False)
    name: str
    record: Record = Record(0, 0, 0)

    def __post_init__(self) -> None:
        self.sort_index = self.record
