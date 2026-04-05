from django import template

register = template.Library()

@register.filter
def total_sum(queryset, field_name):
    return sum(getattr(item, field_name, 0) for item in queryset)
