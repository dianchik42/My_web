from .models import Category, TagPost
from django.db.models import Count

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить материал', 'url_name': 'add_material_model'},
    {'title': 'Методические пособия', 'url_name': 'methodology'},
    {'title': 'Для учителей', 'url_name': 'for_teachers'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
]


class DataMixin:
    """Миксин для передачи общих данных в шаблоны классов представлений"""
    
    def get_mixin_context(self, context, **kwargs):
        """Добавляет общие данные в контекст шаблона"""
        context['mainmenu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context