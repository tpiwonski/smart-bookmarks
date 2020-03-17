from django import template

register = template.Library()


@register.inclusion_tag('ui/templatetags/search_highlights.html')
def search_highlights(highlights):
    return {
        'highlights': highlights
    }
