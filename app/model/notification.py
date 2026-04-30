import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable
from app.services.util import generate_unique_id

class NotificationError(Exception):
    ...

class ChannelUnavailable(NotificationError):
    is_available = False

class DeliveryError(NotificationError):
    ...

@runtime_checkable
class NotificationChanel:
    def send(self, message: str) -> None:
        ...

    def get_channel_name(self) -> str:
        ...

    def is_available(self) -> bool:
        ...
