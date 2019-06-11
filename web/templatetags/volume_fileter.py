from django import template
register = template.Library()

@register.filter
def volume_filter(value):
    if int(value) > 1024 * 1024 * 1024:
        volume = str(round(value / (1024 * 1024 * 1024), 2)) + 'GB'
    elif int(value) > 1024 * 1024:
        volume = str(round(value/(1024 * 1024), 2)) + 'MB'
    elif int(value) > 1024:
        volume = str(round(value/1024, 2)) + 'KB'
    else:
        volume = str(round(value, 2)) + 'By'
    return volume