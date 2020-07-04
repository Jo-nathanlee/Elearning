from django import template
from django.utils.safestring import mark_safe

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
@register.filter
def youtube_url(value):
    if value != '':
        return 'https://www.youtube.com/watch?v='+value
    return value
@register.filter
def shorten_text(value):
    if len(value) <= 10:
        return value
    sliced_word = value[:11]
    returned_text = sliced_word + " ...<a href='/course/lesson/'>More</a>"

    return mark_safe(returned_text)