from dataclasses import dataclass
from typing import Dict, List

from django import template

from smart_bookmarks.ui.utils import reverse_querystring

register = template.Library()


@dataclass
class PaginationInfo:
    view: str
    args: List[any] = None
    kwargs: Dict[str, any] = None
    query: Dict[str, any] = None


@register.filter
def page(pagination: PaginationInfo, page_number: int):
    return reverse_querystring(
        view=pagination.view,
        args=pagination.args,
        kwargs=pagination.kwargs,
        query_kwargs={
            **(pagination.query if pagination.query else {}),
            **{"page": page_number},
        },
    )


def pagination_ctx(
    view: str,
    args: List[any] = None,
    kwargs: Dict[str, any] = None,
    query: Dict[str, any] = None,
):
    return dict(pagination=PaginationInfo(view, args, kwargs, query))
