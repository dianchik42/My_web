from django.db import models
from django.urls import reverse

class PublishedModel(models.Manager):
    """Менеджер для получения только опубликованных материалов"""
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Material.Status.PUBLISHED)


# НОВОЕ ДЛЯ ЛАБЫ: Модель категорий (связь многие к одному)
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


# НОВОЕ ДЛЯ ЛАБЫ: Модель тегов (связь многие ко многим)
class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['tag']

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


# НОВОЕ ДЛЯ ЛАБЫ: Модель для расширения (связь один к одному)
class MaterialExtraInfo(models.Model):
    """Дополнительная информация о материале (связь один к одному)"""
    # Уровень сложности
    difficulty_level = models.CharField(max_length=50, blank=True, verbose_name="Уровень сложности",
                                        choices=[
                                            ('beginner', 'Начальный'),
                                            ('intermediate', 'Средний'),
                                            ('advanced', 'Продвинутый'),
                                        ])
    # Продолжительность в минутах
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, verbose_name="Продолжительность (мин)")
    # Рекомендуемый возраст
    recommended_age = models.CharField(max_length=50, blank=True, verbose_name="Рекомендуемый возраст")
    # Количество скачиваний
    downloads_count = models.IntegerField(default=0, verbose_name="Количество скачиваний")
    # Формат материала
    material_format = models.CharField(max_length=50, blank=True, verbose_name="Формат материала",
                                        choices=[
                                            ('video', 'Видеоурок'),
                                            ('text', 'Текстовый конспект'),
                                            ('test', 'Интерактивный тест'),
                                            ('presentation', 'Презентация'),
                                            ('worksheet', 'Рабочий лист'),
                                            ('case', 'Кейс'),
                                        ])

    class Meta:
        verbose_name = "Дополнительная информация"
        verbose_name_plural = "Дополнительная информация"

    def __str__(self):
        return f"Доп. инфо для материала"


class Material(models.Model):
    """Модель для образовательных материалов"""
    
    class Status(models.IntegerChoices):
        """Класс перечисления для статуса публикации"""
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    
    # ИЗМЕНЕНО ДЛЯ ЛАБЫ: вместо choices теперь внешний ключ
    # category = models.CharField(max_length=50, choices=Category.choices, 
    #                             default=Category.PROGRAMMING, verbose_name="Категория")
    
    # НОВОЕ ДЛЯ ЛАБЫ: связь многие к одному (ForeignKey)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, 
                            verbose_name="Категория", related_name='materials', null=True)
    
    # НОВОЕ ДЛЯ ЛАБЫ: связь многие ко многим (ManyToManyField)
    tags = models.ManyToManyField('TagPost', blank=True, verbose_name="Теги", 
                                   related_name='materials')
    
    # НОВОЕ ДЛЯ ЛАБЫ: связь один к одному (OneToOneField)
    extra_info = models.OneToOneField('MaterialExtraInfo', on_delete=models.SET_NULL, 
                                       null=True, blank=True, verbose_name="Дополнительная информация",
                                       related_name='material')
    
    # Поля модели (остаются без изменений)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Содержание")
    short_description = models.CharField(max_length=500, blank=True, 
                                         verbose_name="Краткое описание")
    author = models.CharField(max_length=100, blank=True, verbose_name="Автор")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, 
                                       verbose_name="Опубликовано")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    
    # Менеджеры
    objects = models.Manager()
    published = PublishedModel()
    
    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
            models.Index(fields=['slug']),
            #models.Index(fields=['cat']),
        ]
        verbose_name = "Образовательный материал"
        verbose_name_plural = "Образовательные материалы"
    
    def get_absolute_url(self):
        return reverse('material', kwargs={'material_slug': self.slug})
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        """Увеличивает счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])