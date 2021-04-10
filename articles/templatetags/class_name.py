from django import template

register = template.Library()


@register.filter()
def class_name(value):
    return value.__class__.__name__

@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg,'')

