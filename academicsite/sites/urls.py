from django.urls import path, register_converter, include
from django.contrib import admin
from . import views, converters

register_converter(converters.FourDigitYearConverter, 'year')
register_converter(converters.TwoDigitMonthConverter, 'month')
register_converter(converters.PositiveIntConverter, 'posint')

urlpatterns = [
    # Основные страницы
    path('', views.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('material/<slug:material_slug>/', views.MaterialDetailView.as_view(), name='material'),
    path('methodology/', views.methodology, name='methodology'),
    path('for_teachers/', views.for_teachers, name='for_teachers'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    
    path('category/<slug:cat_slug>/', views.CategoryMaterialsView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagMaterialsView.as_view(), name='tag'),
    path('add-page/', views.addpage, name='add_page'),
    path('upload/', views.upload_file, name='upload_file'),

    # ДИНАМИЧЕСКИЕ URL
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/', views.article_by_slug, name='article_by_slug'),
    path('category/<str:category>/<int:year>/', views.article_by_category, name='article_by_category'),

    # ИСПОЛЬЗОВАНИЕ СОБСТВЕННЫХ КОНВЕРТЕРОВ
    path('articles/<year:year>/', views.articles_by_year, name='articles_by_year'),
    path('articles/<year:year>/<month:month>/', views.articles_by_year_month, name='articles_by_year_month'),
    path('item/<posint:id>/', views.get_article, name='get_article'),

    # ПЕРЕНАПРАВЛЕНИЯ
    path('old-article/<int:article_id>/', views.old_article_redirect, name='old_article'),
    path('perm-redirect/', views.permanent_redirect, name='perm_redirect'),

    # РАБОТА С ЗАПРОСАМИ
    path('request-info/', views.process_request, name='request_info'),

    # ОБРАБОТКА ИСКЛЮЧЕНИЙ
    path('article-safe/<int:article_id>/', views.get_article, name='article_safe'),
    path('divide/', views.safe_division, name='divide'),

    # ФОРМЫ
    path('add-material/', views.add_material, name='add_material'),
    path('add-material-model/', views.AddMaterialCreateView.as_view(), name='add_material_model'),
    path('edit/<int:pk>/', views.UpdateMaterialView.as_view(), name='edit_material'),
    path('delete/<int:pk>/', views.DeleteMaterialView.as_view(), name='delete_material'),
    ]

handler404 = 'sites.views.page_not_found'