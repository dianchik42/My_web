from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.db.models import Q, F, Count, Avg, Max, Min, Sum, Value
from django.db.models.functions import Length
from .models import Material, Category, TagPost, MaterialExtraInfo
from .forms import AddMaterialModelForm
from django.shortcuts import redirect
import uuid
import os
from django.conf import settings
from .forms import UploadFileForm

# Данные для меню
menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить материал (форма)', 'url_name': 'add_material'},
    {'title': 'Добавить материал (ModelForm)', 'url_name': 'add_material_model'},
    {'title': 'Загрузить файл', 'url_name': 'upload_file'},
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
        'cat_selected': material.cat.pk if material.cat else None,
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

def add_material(request):
    if request.method == 'POST':
        form = AddMaterialForm(request.POST)
        if form.is_valid():
            # Выводим очищенные данные в консоль для проверки
            print("Данные формы:", form.cleaned_data)
            # Пока просто выводим сообщение об успехе
            return render(request, 'sites/add_material.html', {
                'form': form,
                'title': 'Добавление материала',
                'menu': menu,
                'success_message': 'Форма прошла валидацию! Данные не сохранены в БД (несвязанная форма).'
            })
    else:
        form = AddMaterialForm()
    
    return render(request, 'sites/add_material.html', {
        'form': form,
        'title': 'Добавление материала',
        'menu': menu
    })

def add_material_model(request):
    if request.method == 'POST':
        form = AddMaterialModelForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save()
            print(f"✅ Сохранён материал: {material.title}")
            print(f"✅ Категория: {material.cat.name if material.cat else 'НЕ УСТАНОВЛЕНА'}")
            return redirect('home')
        else:
            print("Ошибки формы:", form.errors)
    else:
        form = AddMaterialModelForm()
    
    return render(request, 'sites/add_material_model.html', {
        'form': form,
        'title': 'Добавление материала (связанная форма)',
        'menu': menu
    })

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

def handle_uploaded_file(f):
    # Получаем оригинальное имя файла
    name = f.name
    
    # Разделяем имя и расширение
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    
    # Генерируем уникальный суффикс
    suffix = str(uuid.uuid4())[:8]
    
    # Формируем новое имя файла
    new_filename = f"{name}_{suffix}{ext}"
    
    # Создаём папку uploads, если её нет
    upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Полный путь к файлу
    file_path = os.path.join(upload_dir, new_filename)
    
    # Сохраняем файл по частям (chunks)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return new_filename

def upload_file(request):
    uploaded_filename = None
    error_message = None
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Получаем загруженный файл из формы
            uploaded_file = form.cleaned_data['file']
            
            # Сохраняем файл с уникальным именем
            filename = handle_uploaded_file(uploaded_file)
            uploaded_filename = filename
            
            print(f"Файл сохранён: {filename}")
        else:
            error_message = "Ошибка валидации формы. Пожалуйста, выберите файл."
    else:
        form = UploadFileForm()
    
    return render(request, 'sites/upload_file.html', {
        'form': form,
        'title': 'Загрузка файлов на сервер',
        'menu': menu,
        'uploaded_filename': uploaded_filename,
        'error_message': error_message
    })