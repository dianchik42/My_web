from django.contrib import admin
from django.urls import path, include
from sites import views

handler404 = 'sites.views.page_not_found'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sites.urls')),
    path('about/', views.about, name='about'),
]