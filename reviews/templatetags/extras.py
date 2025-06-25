from django import template

register = template.Library()


@register.filter
def star_range(value):
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return []


@register.filter
def subtract(value, arg):
    """5 - 3 → range(2) → ☆ ☆"""
    try:
        return range(int(value) - int(arg))
    except (ValueError, TypeError):
        return []
