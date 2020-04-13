from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def page(context, page_number):
    query = context.request.GET.copy()
    query["page"] = page_number
    query_string = urlencode(query)
    return f"?{query_string}"
