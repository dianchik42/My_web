from .models import Category, TagPost
from django.db.models import Count
from django.core.exceptions import PermissionDenied

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

class UserIsAuthorMixin:
    """Миксин для проверки, что текущий пользователь является автором материала"""
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Суперпользователь может всё
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # Обычный пользователь может редактировать/удалять только свои материалы
        if obj.author != request.user:
            raise PermissionDenied('Вы не можете редактировать или удалять чужие материалы')
        return super().dispatch(request, *args, **kwargs)