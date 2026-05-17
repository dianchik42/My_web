from django.contrib import admin
from django.urls import path, include
from sites import views

handler404 = 'sites.views.page_not_found'
admin.site.site_header = "Панель администрирования образовательных материалов"
admin.site.index_title = "Управление контентом"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sites.urls')),
    path('about/', views.about, name='about'),
]