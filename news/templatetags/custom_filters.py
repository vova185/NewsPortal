from django import template

register = template.Library()

censor_list = ['Период', 'Загадочный', 'НАЧАЛО',]

@register.filter()
def censor(value):
    for word in censor_list:
        value = value.replace(word[1:], '*' * len(word[1:]))
    return value

forbidden_words = ['кольцо', 'Алтай', 'Злой', ]
@register.filter()
def hide(val):
    v = val.split()
    for word in v:
        if word in forbidden_words:
            val = val.replace(word[1:-1], '*' * len(word[1:-1]))
    return val