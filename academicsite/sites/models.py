from django.db import models
from django.urls import reverse

class PublishedModel(models.Manager):
    """Менеджер для получения только опубликованных материалов"""
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Material.Status.PUBLISHED)


class Material(models.Model):
    """Модель для образовательных материалов"""
    
    class Status(models.IntegerChoices):
        """Класс перечисления для статуса публикации"""
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    
    class Category(models.TextChoices):
        """Класс перечисления для категорий материалов"""
        PROGRAMMING = 'programming', 'Программирование'
        DESIGN = 'design', 'Дизайн'
        MARKETING = 'marketing', 'Маркетинг'
        DATA_SCIENCE = 'data_science', 'Data Science'
        WEB_DEV = 'web_dev', 'Веб-разработка'
        MOBILE_DEV = 'mobile_dev', 'Мобильная разработка'
    
    # Поля модели
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name="URL")
    category = models.CharField(max_length=50, choices=Category.choices, 
                                default=Category.PROGRAMMING, verbose_name="Категория")
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
        ordering = ['-time_create']  # Сортировка по убыванию времени создания
        indexes = [
            models.Index(fields=['-time_create']),
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
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