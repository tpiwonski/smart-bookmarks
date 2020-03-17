from django import template

register = template.Library()


@register.inclusion_tag('ui/templatetags/bookmark_card.html')
def bookmark_card(bookmark):
    return {
        'bookmark': bookmark
    }
