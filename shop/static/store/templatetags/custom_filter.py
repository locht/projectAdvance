
from django import template
from ..models import *

register = template.Library()

@register.filter
def getChilds(parentId):
    return Category.objects.filter(cate_parent_id=parentId)

@register.filter
def hasChilds(parentId):
    childs = Category.objects.filter(cate_parent_id=parentId)
    if childs is not None:
        if len(childs) > 0:
            return "True"
    else:
        return "False"
