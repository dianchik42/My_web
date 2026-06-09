from django import forms
from django.core.exceptions import ValidationError
from .models import Material, Category, TagPost, MaterialExtraInfo

# Пользовательский валидатор для проверки русских и английских букв
def validate_title(value):
    allowed_chars = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 -"
    for char in value:
        if char not in allowed_chars:
            raise ValidationError(
                'Допустимы только русские и английские буквы, цифры, дефис и пробел. '
                f'Недопустимый символ: "{char}"'
            )
    return value

class AddMaterialForm(forms.Form):

    title = forms.CharField(
        max_length=100,
        min_length=5,
        label="Заголовок",
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        validators=[validate_title],
        error_messages={
            'min_length': 'Заголовок должен содержать минимум 5 символов',
            'max_length': 'Заголовок не может быть длиннее 100 символов',
            'required': 'Поле "Заголовок" обязательно для заполнения'
        }
    )
    slug = forms.SlugField(
        max_length=255,
        min_length=5,
        label="URL (slug)",
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        error_messages={
            'min_length': 'Slug должен содержать минимум 5 символов',
            'required': 'Поле "URL" обязательно для заполнения'
        }
    )
    content = forms.CharField(
        label="Содержание",
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        required=False
    )
    short_description = forms.CharField(
        label="Краткое описание",
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        required=False
    )
    author = forms.CharField(
        max_length=100,
        label="Автор",
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        required=False
    )
    is_published = forms.BooleanField(
        label="Опубликовано",
        required=False,
        initial=True
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория",
        empty_label="Выберите категорию",
        error_messages={
            'required': 'Пожалуйста, выберите категорию'
        }
    )


# ФОРМА, СВЯЗАННАЯ С МОДЕЛЬЮ
class AddMaterialModelForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'slug', 'content', 'short_description', 
                  'is_published', 'cat', 'tags', 'extra_info', 'image']
        
        labels = {
            'title': 'Заголовок',
            'slug': 'URL (slug)',
            'content': 'Содержание',
            'short_description': 'Краткое описание',
            'author': 'Автор',
            'is_published': 'Опубликовано',
            'cat': 'Категория',
            'tags': 'Теги',
            'extra_info': 'Дополнительная информация',
            'image': 'Изображение',
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'short_description': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
            'author': forms.TextInput(attrs={'class': 'form-input'}),
            'cat': forms.Select(attrs={'class': 'form-input'}),  # Важно: cat, а не category
            'extra_info': forms.Select(attrs={'class': 'form-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }
        
        error_messages = {
            'title': {
                'required': 'Поле "Заголовок" обязательно для заполнения',
                'max_length': 'Заголовок не может быть длиннее 255 символов',
            },
            'slug': {
                'required': 'Поле "URL" обязательно для заполнения',
                'unique': 'Материал с таким URL уже существует',
            },
            'cat': {
                'required': 'Пожалуйста, выберите категорию',
            },
        }
    
    # Поле tags сделаем удобным для выбора
    tags = forms.ModelMultipleChoiceField(
        queryset=TagPost.objects.all(),
        label="Теги",
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 5, 'class': 'form-input'})
    )
    
    # Собственный валидатор для поля title
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            return title
        
        if len(title) < 5:
            raise ValidationError('Заголовок должен содержать минимум 5 символов')
        
        allowed_chars = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 -"
        for char in title:
            if char not in allowed_chars:
                raise ValidationError(f'Допустимы только русские и английские буквы, цифры, дефис и пробел. Недопустимый символ: "{char}"')
        
        return title
    
    # Собственный валидатор для поля author
    def clean_author(self):
        author = self.cleaned_data.get('author')
        if not author:
            return author
        
        allowed_chars = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -"
        for char in author:
            if char not in allowed_chars:
                raise ValidationError(f'В имени автора допустимы только русские и английские буквы, дефис и пробел. Недопустимый символ: "{char}"')
        
        return author

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="Выберите файл",
        widget=forms.FileInput(attrs={'class': 'form-input'}),
        help_text="Максимальный размер файла: 10 МБ"
    )