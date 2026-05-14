from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from .models import Material
from django.shortcuts import get_object_or_404

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

# Рубрики
cats_db = [
    {'id': 1, 'name': 'Математика'},
    {'id': 2, 'name': 'Русский язык'},
    {'id': 3, 'name': 'Литература'},
    {'id': 4, 'name': 'История'},
    {'id': 5, 'name': 'Обществознание'},
    {'id': 6, 'name': 'Физика'},
    {'id': 7, 'name': 'Химия'},
    {'id': 8, 'name': 'Биология'},
    {'id': 9, 'name': 'Информатика'},
    {'id': 10, 'name': 'Иностранные языки'},
    {'id': 11, 'name': 'Начальная школа'},
    {'id': 12, 'name': 'Внеурочная деятельность'},
]


def index(request):
    """Главная страница"""
    posts = Material.objects.filter(is_published=Material.Status.PUBLISHED)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
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


def show_category(request, cat_id):
    """Отображение статей по категории"""
    posts = Material.objects.filter(is_published=Material.Status.PUBLISHED)
    data = {
        'title': 'Отображение по рубрики/категории',
        'menu': menu,
        'posts': posts,
        'cat_selected': cat_id,
    }
    return render(request, 'sites/index.html', context=data)


def show_material(request, material_slug):
    material = get_object_or_404(Material, slug=material_slug, is_published=Material.Status.PUBLISHED)
    return render(request, 'sites/material_detail.html', {'material': material})


def materials(request):
    """Страница со всеми учебными материалами"""
    posts = Material.objects.filter(is_published=Material.Status.PUBLISHED)
    data = {
        'title': 'Учебные материалы',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'sites/index.html', context=data)


def methodology(request):
    """Страница с методическими пособиями"""
    posts = Material.published.all()
    data = {
        'title': 'Методические пособия',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'sites/index.html', context=data)


def for_teachers(request):
    """Страница для учителей"""
    posts = Material.published.all()
    data = {
        'title': 'Для учителей',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'sites/index.html', context=data)

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