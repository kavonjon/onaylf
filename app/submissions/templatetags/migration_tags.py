from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def find_by_id(items, item_id):
    for item in items:
        if item['id'] == item_id:
            return item
    return None