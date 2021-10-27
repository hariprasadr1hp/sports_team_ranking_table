from __future__ import annotations

import enum


@enum.unique
class Result(enum.Enum):
    LOSS = enum.auto()
    DRAW = enum.auto()
    WIN = enum.auto()
