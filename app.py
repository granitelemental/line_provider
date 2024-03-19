import time
from http import HTTPStatus
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.params import Depends
from publisher import RabbitPublisher
from basic_types import Event, EventFilter
from utils import repeat_every
from repositories import InMemoryEventRepository
from exceptions import EventNotFound, EventExists, RabbitConnectionFailed
from constants import EventState
from config import RabbitConfig
from base import logger


# нужно проверить рейс кондишены
event_repo = InMemoryEventRepository(
    events={
        '1': Event(
            event_id='1', coefficient=1.2, deadline=int(time.time()) + 600, state=EventState.NEW, is_sent=False,
        ),
        '2': Event(
            event_id='2', coefficient=1.15, deadline=int(time.time()) + 60, state=EventState.NEW, is_sent=False,
        ),
        '3': Event(
            event_id='3', coefficient=1.67, deadline=int(time.time()) + 90, state=EventState.NEW, is_sent=False,
        )
    }
)

app = FastAPI()
rabbit_config = RabbitConfig()
publisher = RabbitPublisher(config=rabbit_config)


@app.on_event("startup")
async def on_startup():
    try:
        await publisher.connect()
    except RabbitConnectionFailed:
        logger.error('Не удалось подключиться к Rabbit')
    else:
        @repeat_every(seconds=rabbit_config.INTERVAL_TO_SLEEP_SEC)
        async def publish_events() -> None:
            await publisher.publish_events_if_exist(events=event_repo.events)

        await publish_events()


@app.on_event("shutdown")
async def app_shutdown():
    await publisher.disconnect()


@app.post('/event')
async def create_event(event: Event):
    try:
        event_repo.add(event)
    except EventExists:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=f"Event with id: {event.event_id} already exists")

    return {'event_id': event.event_id}


@app.put('/event')
async def create_or_update_event(event: Event):
    try:
        event_repo.update(event)
    except EventNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Event with id {event.event_id} not found")

    return {'event_id': event.event_id}


@app.get('/event/{event_id}')
async def get_event(event_id: str = Path()):
    try:
        return event_repo.get_by_id(event_id)
    except EventNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Event with id {event_id} not found")


@app.get('/events')
async def get_events(
        limit: int = Query(100),
        offset: int = Query(0),
        event_filter: EventFilter = Depends(),
):
    return event_repo.get_list(limit=limit, offset=offset, event_filter=event_filter)
