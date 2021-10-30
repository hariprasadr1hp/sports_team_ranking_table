from __future__ import annotations
from dataclasses import dataclass, field

from src.record import Record


@dataclass(order=True)
class Team:
    """
    Name the team and an account of its records

    """
    sort_index: str = field(init=False, repr=False)
    name: str = field(compare=True)
    record: Record = field(default_factory=Record)

    def __post_init__(self, ) -> None:
        self.sort_index = self.name
