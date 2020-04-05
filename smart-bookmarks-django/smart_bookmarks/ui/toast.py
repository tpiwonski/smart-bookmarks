from dataclasses import dataclass

from django.contrib import messages

TOAST_INFO = "info"
TOAST_ERROR = "error"


@dataclass
class Toast:
    message: str
    type: str


@dataclass
class ToastInfo(Toast):
    type: str = TOAST_INFO


@dataclass
class ToastError(Toast):
    type: str = TOAST_ERROR


@dataclass
class Message:
    message: str
    level: str


@dataclass
class ErrorMessage(Message):
    level: str = messages.ERROR


@dataclass
class InfoMessage(Message):
    level: str = messages.INFO
