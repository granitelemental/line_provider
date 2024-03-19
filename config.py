import os
from dotenv import load_dotenv

load_dotenv()


class RabbitConfig:
    RABBIT_HOST = os.getenv('RABBIT_HOST')
    RABBIT_PORT = int(os.getenv('RABBIT_PORT'))
    RABBIT_USER = os.getenv('RABBIT_USER')
    RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')
    QUEUE_NAME = os.getenv('QUEUE_NAME')
    INTERVAL_TO_SLEEP_SEC = int(os.getenv('INTERVAL_TO_SLEEP_SEC'))

