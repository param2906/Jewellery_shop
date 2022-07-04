from django import template

register = template.Library()

@register.filter(name = 'is_in_cart')

def is_in_cart(i, cart):
    keys = cart.keys()
    for id in keys:
        print(type(id , type(i.id)))
        if int(id) == i.id:
            return True
    return False