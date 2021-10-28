import enum

@enum.unique
class IOHandler(enum.Enum):
    NONE = enum.auto()
    CSV = enum.auto()
    SQL = enum.auto()
    PICKLE = enum.auto()


class ReadWriteOper:
    iohandler: IOHandler = IOHandler.NONE
    ...
