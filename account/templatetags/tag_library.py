from django import template

register = template.Library()

@register.filter
def get_filename(value):
    return str(value).replace("files/","")

def to_int(value):
    return int(value)