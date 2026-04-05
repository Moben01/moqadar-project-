import jdatetime
from django import template

register = template.Library()

@register.filter
def to_jalali(value):
    if not value:
        return ""
    try:
        jdate = jdatetime.datetime.fromgregorian(datetime=value)
        return jdate.strftime('%Y/%m/%d - %H:%M %p')
    except Exception:
        return value
