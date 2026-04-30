import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable
from app.services.util import generate_unique_id
from abc import abstractmethod,ABC

class NotificationError(Exception):
    ...

class ChannelUnavailable(NotificationError):
    is_available = False

class DeliveryError(NotificationError):
    ...

@runtime_checkable
class NotificationChanel(ABC):
    def send(self, message: str) -> None:
        ...

    def get_channel_name(self) -> str:
        ...

    def is_available(self) -> bool:
        ...

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

    @abstractmethod
    def get_channel_name(self) -> str: ...

    @abstractmethod
    def is_available(self) -> bool: ...