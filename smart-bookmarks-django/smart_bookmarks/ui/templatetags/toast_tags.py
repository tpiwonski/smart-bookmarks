from dataclasses import dataclass

from django import template

register = template.Library()


TOAST_INFO = 'info'
TOAST_ERROR = 'error'


@dataclass
class Toast:
    type: str
    message: str


@register.inclusion_tag('ui/templatetags/toast.html')
def toast(toast_data):
    return {
        'toast': toast_data
    }
