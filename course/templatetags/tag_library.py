from django import template

register = template.Library()

@register.filter
def get_filename(value):
    return str(value).replace("files/","")
@register.filter
def to_int(value):
    return int(value)
@register.filter
def to_str(value):
    return str(value)