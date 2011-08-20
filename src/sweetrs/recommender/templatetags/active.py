from django.template import Library

__author__ = 'kidzik'

register = Library()

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''