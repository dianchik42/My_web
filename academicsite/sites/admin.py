from django.contrib import admin
from django.contrib import messages
from .models import Material, Category, TagPost, MaterialExtraInfo

class ViewsCountFilter(admin.SimpleListFilter):
    title = 'Количество просмотров'
    parameter_name = 'views'

    def lookups(self, request, model_admin):
        return [
            ('low', 'Менее 10 просмотров'),
            ('medium', '10-50 просмотров'),
            ('high', 'Более 50 просмотров'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(views_count__lt=10)
        if self.value() == 'medium':
            return queryset.filter(views_count__gte=10, views_count__lte=50)
        if self.value() == 'high':
            return queryset.filter(views_count__gt=50)
        return queryset

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cat', 'is_published', 'time_create', 'views_count', 'short_content', 'title_length')
    list_display_links = ('id', 'title')
    ordering = ('-time_create', 'title')
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['publish_selected', 'unpublish_selected']
    search_fields = ('title', 'cat__name', 'author', 'content')
    list_filter = ('is_published', 'cat', 'time_create', ViewsCountFilter)
    filter_horizontal = ('tags',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'cat', 'author')
        }),
        ('Содержание', {
            'fields': ('short_description', 'content'),
            'classes': ('wide',)
        }),
        ('Публикация и статистика', {
            'fields': ('is_published', 'views_count'),
            'classes': ('collapse',)
        }),
        ('Связи', {
            'fields': ('tags', 'extra_info'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('views_count',)

    @admin.display(description="Краткое содержание")
    def short_content(self, obj):
        if len(obj.content) > 50:
            return obj.content[:50] + "..."
        return obj.content[:50]

    @admin.display(description="Длина заголовка")
    def title_length(self, obj):
        return len(obj.title)

    @admin.action(description="Опубликовать выбранные материалы")
    def publish_selected(self, request, queryset):
        count = queryset.update(is_published=Material.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} материалов.", messages.SUCCESS)

    @admin.action(description="Снять с публикации выбранные материалы")
    def unpublish_selected(self, request, queryset):
        count = queryset.update(is_published=Material.Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} материалов.", messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    search_fields = ('tag',)
    prepopulated_fields = {'slug': ('tag',)}
    ordering = ('tag',)

@admin.register(MaterialExtraInfo)
class MaterialExtraInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'difficulty_level', 'duration_minutes', 'downloads_count')
    list_display_links = ('id',)
    list_editable = ('difficulty_level', 'duration_minutes', 'downloads_count')
    search_fields = ('difficulty_level',)