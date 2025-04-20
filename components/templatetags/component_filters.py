from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def filter(queryset, lookup):
    """Filter a queryset based on a lookup expression"""
    if not queryset:
        return []
    return queryset.filter(**{lookup: True})

@register.filter
def sum(queryset, field):
    """Sum a field across a queryset"""
    if not queryset:
        return 0
    return sum(getattr(obj, field) for obj in queryset)

@register.filter
def sub(value, arg):
    """Subtract arg from value"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0 