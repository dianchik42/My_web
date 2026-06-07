from django.db import models
from django.urls import reverse

class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Material.Status.PUBLISHED)

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

class MaterialExtraInfo(models.Model):
    difficulty_level = models.CharField(max_length=50, blank=True, verbose_name="Уровень сложности")
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, verbose_name="Продолжительность (мин)")
    downloads_count = models.IntegerField(default=0, verbose_name="Количество скачиваний")

    class Meta:
        verbose_name = "Дополнительная информация"
        verbose_name_plural = "Дополнительная информация"

    def __str__(self):
        return f"Инфо для материала (скачиваний: {self.downloads_count})"

class Material(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Содержание")
    short_description = models.CharField(max_length=500, blank=True, verbose_name="Краткое описание")
    author = models.CharField(max_length=100, blank=True, verbose_name="Автор")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Опубликовано")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")

    # НОВОЕ ПОЛЕ ДЛЯ ИЗОБРАЖЕНИЯ
    image = models.ImageField(
        upload_to='materials_images/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name="Изображение"
    )

    # Связи
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True,
                           verbose_name="Категория", related_name='materials')
    tags = models.ManyToManyField(TagPost, blank=True, verbose_name="Теги", related_name='materials')
    extra_info = models.OneToOneField(MaterialExtraInfo, on_delete=models.SET_NULL,
                                      null=True, blank=True, verbose_name="Дополнительная информация",
                                      related_name='material')

    objects = models.Manager()
    published = PublishedModel()

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
            models.Index(fields=['slug']),
        ]
        verbose_name = "Образовательный материал"
        verbose_name_plural = "Образовательные материалы"

    def get_absolute_url(self):
        return reverse('material', kwargs={'material_slug': self.slug})

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])