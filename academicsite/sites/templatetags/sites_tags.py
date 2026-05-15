from django import template
from django.db.models import Count
from sites.models import Category, TagPost

register = template.Library()

@register.inclusion_tag('sites/list_categories.html')
def show_categories(cat_selected=0):
    # Только категории, у которых есть хотя бы один опубликованный материал
    cats = Category.objects.annotate(total=Count('materials')).filter(
        total__gt=0,
        materials__is_published=1
    ).distinct()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('sites/list_tags.html')
def show_tags():
    # Только теги, у которых есть хотя бы один опубликованный материал
    tags = TagPost.objects.annotate(total=Count('materials')).filter(
        total__gt=0,
        materials__is_published=1
    ).distinct()
    return {'tags': tags}