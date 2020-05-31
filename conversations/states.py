import enum


class AddTaskConvState(enum.Enum):
    ASK_NAME = enum.auto(),
    ASK_PARTICIPANTS = enum.auto()


class CheckTaskConvState(enum.Enum):
    ASK_NAME = enum.auto()


class DeleteTaskConvState(enum.Enum):
    ASK_NAME = enum.auto()
