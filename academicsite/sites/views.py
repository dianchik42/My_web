from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.db.models import Q, F, Count, Avg, Max, Min, Sum, Value
from django.db.models.functions import Length
from .models import Material, Category, TagPost, MaterialExtraInfo

# Данные для меню
menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить материалы', 'url_name': 'add_page'},
    {'title': 'Методические пособия', 'url_name': 'methodology'},
    {'title': 'Для учителей', 'url_name': 'for_teachers'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]


def index(request):
    """Главная страница"""
    posts = Material.published.all().select_related('cat').prefetch_related('tags')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'sites/index.html', context=data)


def about(request):
    """Страница О сайте"""
    data = {
        'title': 'О сайте',
        'menu': menu,
        'cat_selected': 0,
    }
    return render(request, 'sites/about.html', context=data)


def addpage(request):
    """Добавление статьи"""
    return HttpResponse("Добавление статьи")


def contact(request):
    """Обратная связь"""
    return HttpResponse("Обратная связь")


def login(request):
    """Авторизация"""
    return HttpResponse("Авторизация")


# отображение по категориям
def show_category(request, cat_slug):
    """Отображение материалов по категории"""
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Material.published.filter(cat=category)
    data = {
        'title': f'Категория: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'sites/index.html', context=data)

def show_tag(request, tag_slug):
    """Отображение материалов по тегу"""
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.materials.filter(is_published=Material.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'sites/index.html', context=data)

def show_material(request, material_slug):
    """Отображение отдельного материала"""
    material = get_object_or_404(Material, slug=material_slug, is_published=Material.Status.PUBLISHED)
    material.increment_views()
    data = {
        'material': material,
        'title': material.title,
        'menu': menu,
        'cat_selected': material.cat.pk,
    }
    return render(request, 'sites/material_detail.html', context=data)


def materials(request):
    """Страница со всеми учебными материалами"""
    posts = Material.published.all().select_related('cat').prefetch_related('tags')
    data = {
        'title': 'Учебные материалы',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'sites/index.html', context=data)


def methodology(request):
    """Страница с методическими пособиями"""
    posts = Material.published.all().select_related('cat').prefetch_related('tags')
    data = {
        'title': 'Методические пособия',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'sites/index.html', context=data)


def for_teachers(request):
    """Страница для учителей"""
    posts = Material.published.all().select_related('cat').prefetch_related('tags')
    data = {
        'title': 'Для учителей',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'sites/index.html', context=data)


def orm_examples(request):
    """Страница для демонстрации ORM-методов"""
    return HttpResponse("ORM примеры")


# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def article_detail(request, article_id):
    return HttpResponse(f"Статья №{article_id}")


def article_by_category(request, category, year):
    return HttpResponse(f"Категория: {category}, год: {year}")


def article_by_slug(request, slug):
    return HttpResponse(f"Статья: {slug}")


def old_article_redirect(request, article_id):
    return redirect(f'/article/{article_id}/')


def permanent_redirect(request):
    return HttpResponseRedirect('/sites/', status=301)


@require_http_methods(['GET', 'POST'])
def process_request(request):
    method = request.method
    search_query = request.GET.get('q', '')
    if method == 'POST':
        name = request.POST.get('name', '')
        return HttpResponse(f"POST запрос от {name}")
    return HttpResponse(f"GET запрос, поиск: {search_query}")


def get_article(request, article_id):
    try:
        if article_id not in [1, 2, 3]:
            raise KeyError
        return HttpResponse(f"Статья {article_id}")
    except KeyError:
        return HttpResponseNotFound(f"Статья {article_id} не найдена")


def safe_division(request):
    try:
        a = int(request.GET.get('a', 0))
        b = int(request.GET.get('b', 1))
        result = a / b
        return HttpResponse(f"Результат: {result}")
    except (ValueError, ZeroDivisionError) as e:
        return HttpResponseNotFound(f"Ошибка: {str(e)}")


def articles_by_year(request, year):
    return HttpResponse(f"Статьи за {year} год")


def articles_by_year_month(request, year, month):
    return HttpResponse(f"Статьи за {year}/{month}")


def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена (404)")