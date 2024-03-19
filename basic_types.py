import decimal

from typing import Optional
from constants import EventState, EventOrderFields
from pydantic import BaseModel


class EventFilter(BaseModel):
    is_sent: Optional[bool] = None


class Event(BaseModel):
    event_id: str
    coefficient: Optional[decimal.Decimal] = None
    deadline: Optional[int] = None
    state: Optional[EventState] = None
    is_sent: Optional[bool] = None

    def as_dict(self):
        return {
            'event_id': self.event_id,
            'coefficient': float(self.coefficient),
            'deadline': self.deadline,
            'state': str(self.state.name),
            'is_sent': self.is_sent,
        }

