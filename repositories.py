from abc import ABC, abstractmethod
from copy import deepcopy
from datetime import datetime
import time
from typing import Optional
from basic_types import Event, EventFilter
from constants import EventState, EventOrderFields
from exceptions import EventNotFound, EventExists


class BaseEventRepository(ABC):
    @abstractmethod
    def get_by_id(self, event_id: int) -> Event: ...

    @abstractmethod
    def add(self, event: Event): ...

    @abstractmethod
    def update(self, event_data: Event): ...

    @abstractmethod
    def get_list(
            self,
            *,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            event_filter: EventFilter,
    ): ...


class InMemoryEventRepository(BaseEventRepository):
    def __init__(self, events: dict[str, Event]):
        self.events = events

    def get_by_id(self, event_id: str) -> Event:
        if event_id not in self.events:
            raise EventNotFound

        return self.events[event_id]

    def add(self, event: Event):
        if event.event_id in self.events:
            raise EventExists

        self.events[event.event_id] = event

    def update(self, event_data: Event):
        if event_data.event_id not in self.events:
            raise EventNotFound

        for p_name, p_value in event_data.dict(exclude_unset=True).items():
            setattr(self.events[event_data.event_id], p_name, p_value)

    def get_list(
            self,
            *,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            event_filter: Optional[EventFilter] = None,
    ):
        result = [v for _, v in self.events.items()]
        # result = filter(lambda x: x.deadline > datetime.timestamp(datetime.utcnow()), result)

        if event_filter.is_sent is not None:
            result = filter(lambda x: x.is_sent is event_filter.is_sent, result)

        result = list(result)

        if offset is not None:
            result = result[offset:]

        if limit is not None:
            result = result[:limit]

        return result

