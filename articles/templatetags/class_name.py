from django import template

register = template.Library()


@register.filter()
def class_name(value):
    return value.__class__.__name__

@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg,'')

@register.filter
def mul(value, arg):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = float(value)
        arg = float(arg)
        if arg:
            return format(value * arg, '.2f')
    except:
        pass
    return ''