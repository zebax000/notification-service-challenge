import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable
from app.services.util import generate_unique_id
from abc import abstractmethod,ABC

class NotificationError(Exception):
    ...

class ChannelUnavailable(NotificationError):
    ...

class DeliveryError(NotificationError):
    ...

@runtime_checkable
class NotificationChannel(ABC):

    @abstractmethod
    def send(self, message: str) -> None:
        pass

    @abstractmethod
    def get_channel_name(self) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

class ConsoleChannel(NotificationChannel):

    def send(self, message: str) -> None:
        try:
            print(message)
        except Exception as e:
            raise DeliveryError(f"Error al enviar por consola: {e}")

    def get_channel_name(self) -> str:
        return "console"

    def is_available(self) -> bool:
        return True

class FileChannel(NotificationChannel):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_channel_name(self) -> str:
        return f"file:{self.file_path}"

    def is_available(self) -> bool:
        if os.path.exists(self.file_path):
            return os.access(self.file_path, os.W_OK)
        parent_dir = os.path.dirname(self.file_path) or "."
        return os.path.isdir(parent_dir) and os.access(parent_dir, os.W_OK)

    def send(self, message: str) -> None:
        if not self.is_available():
            raise ChannelUnavailable(f"Canal no disponible: {self.get_channel_name()}")

        try:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except OSError as e:
            raise DeliveryError(f"error escribiendo en el archivo: {e}")

class MockChannel(NotificationChannel):

    def get_channel_name(self) -> str:
        return "mock"

    def is_available(self) -> bool:
        return False

    def send(self, message: str) -> None:
        raise ChannelUnavailable("el canal mock no esta disponible")

#punto 4#
class NotificationService:
    def __init__(self, _channel: NotificationChannel, ):
        self._channel = NotificationChannel
        self._history: list[str]

    def send_notification(self, message: str) -> None:
        if is_available() == True