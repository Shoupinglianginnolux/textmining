from django import template

register = template.Library()

@register.filter
def percentage(value):
    return format(float(value), ".2%")

@register.filter
def to_and(value):
    return value.replace("-","_")

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 