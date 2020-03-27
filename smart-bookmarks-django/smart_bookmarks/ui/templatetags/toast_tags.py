from dataclasses import dataclass

from django import template

register = template.Library()


TOAST_INFO = 'info'
TOAST_ERROR = 'error'


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


@register.inclusion_tag('ui/templatetags/toast.html')
def toast(toast_data):
    return {
        'toast': toast_data
    }
