from django import template
register = template.Library()

@register.filter(name='lookup')
def lookup(model, attr):
    if hasattr(model, attr):
        return getattr(model, attr)
    else:
        return None

