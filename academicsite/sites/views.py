from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Material, Category, TagPost
from .forms import AddMaterialModelForm
from .utils import DataMixin, menu
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class HomeView(DataMixin, ListView):
    model = Material
    template_name = 'sites/index.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_queryset(self):
        return Material.published.all().select_related('cat').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Главная страница', cat_selected=0)


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
class CategoryMaterialsView(DataMixin, ListView):
    template_name = 'sites/index.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 3
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return Material.published.filter(cat=self.category).select_related('cat')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f'Категория: {self.category.name}', cat_selected=self.category.pk)


class TagMaterialsView(DataMixin, ListView):
    template_name = 'sites/index.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 3
    
    def get_queryset(self):
        self.tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return self.tag.materials.filter(is_published=Material.Status.PUBLISHED).select_related('cat')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f'Тег: {self.tag.tag}')


class MaterialDetailView(DataMixin, DetailView):
    model = Material
    template_name = 'sites/material_detail.html'
    context_object_name = 'material'
    slug_url_kwarg = 'material_slug'
    
    def get_queryset(self):
        return Material.published.all()
    
    def get_object(self, queryset=None):
        material = super().get_object(queryset)
        material.increment_views()
        return material
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_selected = self.object.cat.pk if self.object.cat else None
        return self.get_mixin_context(context, title=self.object.title, cat_selected=cat_selected)


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


class AddMaterialCreateView(LoginRequiredMixin, DataMixin, CreateView):
    """Класс представления для добавления нового материала"""
    model = Material
    form_class = AddMaterialModelForm
    template_name = 'sites/add_material_model.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Добавление материала')
    
    def form_valid(self, form):
        """Автоматически назначает автором текущего пользователя"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateMaterialView(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, UpdateView):
    model = Material
    form_class = AddMaterialModelForm
    template_name = 'sites/edit_material.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'pk'
    permission_required = 'sites.change_material'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Редактирование материала')


class DeleteMaterialView(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, DeleteView):
    model = Material
    template_name = 'sites/delete_material.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'pk'
    permission_required = 'sites.delete_material'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Удаление материала')


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