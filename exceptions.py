class LineProviderException(BaseException):
    pass


class EventNotFound(LineProviderException):
    pass


class EventExists(LineProviderException):
    pass


class RabbitConnectionFailed(LineProviderException):
    pass


class RabbitChannelNotObtained(LineProviderException):
    pass


class PublishingFailed(LineProviderException):
    pass
