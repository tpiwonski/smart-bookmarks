from django import template
from django.core.paginator import Page

from smart_bookmarks.ui.utils import reverse_querystring, ViewInfo

register = template.Library()


@register.inclusion_tag("ui/templatetags/pagination.html")
def pagination(page: Page, view: ViewInfo):
    return {
        'page': page,
        'view': view
    }


@register.filter
def page(view: ViewInfo, page_number: int):
    return reverse_querystring(view=view.viewname, args=view.args, kwargs=view.kwargs,
                               query_kwargs={**(view.query if view.query else {}), **{'page': page_number}})
