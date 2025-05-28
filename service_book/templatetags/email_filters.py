from django import template

register = template.Library()

@register.filter
def mask_email(value):
    if not value or '@' not in value:
        return value
    name, domain = value.split('@', 1)
    if len(name) <= 2:
        masked = name[0] + '*' * (len(name) - 1)
    else:
        masked = name[:2] + '*' * (len(name) - 2)
    return f'{masked}@{domain}'