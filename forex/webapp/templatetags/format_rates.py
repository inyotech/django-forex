from django import template

register = template.Library()

@register.filter
def columns(list_, n):

    try:
        n = int(n)
        list_ = list(list_)
    except (ValueError, TypeError):
        return [list_]
    list_len = len(list_)
    split = list_len // n
    if list_len % n != 0:
        split += 1
    return [list_[i::split] for i in range(split)]
