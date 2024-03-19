from typing import Optional
import aio_pika
import json
from basic_types import Event
from config import RabbitConfig
from exceptions import RabbitConnectionFailed, RabbitChannelNotObtained, PublishingFailed
from base import logger


class RabbitPublisher:
    config: RabbitConfig
    _connection: aio_pika.abc.AbstractRobustConnection
    _channel: aio_pika.abc.AbstractRobustChannel
    _exchange: aio_pika.abc.AbstractExchange

    def __init__(self, config: RabbitConfig):
        self.config = config

    async def connect(self):
        self._connection = await self.get_connection()
        self._channel = await self._connection.channel()
        self._exchange = self._channel.default_exchange

    async def disconnect(self):
        logger.debug('Disconnecting from rabbit...')
        await self._connection.close()
        logger.debug('Disconnected from rabbit')

    async def get_connection(self) -> aio_pika.abc.AbstractRobustConnection:
        try:
            logger.debug('Connecting to rabbit...')
            conn = await aio_pika.connect_robust(
                    f"amqp://{self.config.RABBIT_USER}:"
                    f"{self.config.RABBIT_PASSWORD}@{self.config.RABBIT_HOST}:{self.config.RABBIT_PORT}/"
                )
            logger.debug('Connected to rabbit')
            return conn
        except BaseException:
            raise RabbitConnectionFailed

    @staticmethod
    async def get_channel(conn: aio_pika.abc.AbstractRobustConnection) -> aio_pika.abc.AbstractRobustChannel:
        try:
            return await conn.channel()
        except BaseException:
            raise RabbitChannelNotObtained

    @staticmethod
    def event_to_bytes(event: Event) -> bytes:
        return json.dumps(event.as_dict()).encode()

    async def send_event(self, event: Event):
        try:
            await self._exchange.publish(
                aio_pika.Message(body=self.event_to_bytes(event)),
                routing_key=self.config.QUEUE_NAME,
            )
        except BaseException:
            raise PublishingFailed

    async def publish_events_if_exist(self, events: dict):
        unpublished = [v for _, v in events.items() if v.is_sent is False]
        for v in unpublished:
            logger.debug('Publishing events to channel...')
            await self.send_event(event=v)
            events[v.event_id].is_sent = True
            logger.debug(f'Events are published successfully ({len(unpublished)})')
