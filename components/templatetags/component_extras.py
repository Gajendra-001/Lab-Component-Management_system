from django import template
from django.db.models import QuerySet

register = template.Library()

@register.filter
def div(value, arg):
    """Divide value by arg"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    """Multiply value by arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def active_checkouts(component):
    """Get active checkouts for a component"""
    if not component or not hasattr(component, 'checkouts'):
        return []
    return component.checkouts.filter(actual_return_date__isnull=True)

@register.filter
def checkout_quantity(checkouts):
    """Sum the quantity of checkouts"""
    if not checkouts:
        return 0
    if isinstance(checkouts, QuerySet):
        return sum(checkout.quantity for checkout in checkouts)
    return 0

@register.filter
def available_quantity(component):
    """Calculate available quantity for a component"""
    if not component:
        return 0
    active = active_checkouts(component)
    checked_out = checkout_quantity(active)
    return max(0, component.quantity - checked_out)

@register.filter
def sub(value, arg):
    """Subtract arg from value"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0 