from django.template.defaulttags import register


@register.filter
def inverse(flag):
    return not flag


@register.filter
def cut_title(title: str) -> str:
    return f'{title[:33]}...' if len(title) > 36 else title
