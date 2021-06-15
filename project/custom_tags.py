import json

from django.template.defaulttags import register
from django.utils.safestring import mark_safe


@register.filter
def inverse(flag):
    return not flag


@register.filter
def cut_title(title: str) -> str:
    return f'{title[:33]}...' if len(title) > 36 else title


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))
