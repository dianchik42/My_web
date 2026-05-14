from django import template
from sites import views

register = template.Library()

# Простой тег - возвращает список категорий
@register.simple_tag()
def get_categories():
    return views.cats_db

# Включающий тег - возвращает HTML с категориями
@register.inclusion_tag('sites/list_categories.html')
def show_categories(cat_selected=0):
    cats = views.cats_db
    return {'cats': cats, 'cat_selected': cat_selected}