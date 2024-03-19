import enum


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class EventOrderFields(enum.StrEnum):
    is_sent = 'is_sent'
    is_deleted = 'is_deleted'
    status_id = 'status'

