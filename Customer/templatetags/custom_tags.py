from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def total_sum(queryset, field_name):
    return sum(getattr(item, field_name, 0) for item in queryset)


@register.filter
def balance_difference(value, other_value):
    try:
        return abs(Decimal(value or 0) - Decimal(other_value or 0))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal('0')
