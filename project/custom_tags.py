from django.template.defaulttags import register


@register.filter
def inverse(flag):
    return not flag
