from django.contrib import admin
from django.urls import path, include
from sites import views
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'sites.views.page_not_found'
admin.site.site_header = "Панель администрирования образовательных материалов"
admin.site.index_title = "Управление контентом"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sites.urls')),
    path('about/', views.about, name='about'),
]

# РАЗДАЧА МЕДИА-ФАЙЛОВ (ИЗОБРАЖЕНИЙ) В РЕЖИМЕ ОТЛАДКИ
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)