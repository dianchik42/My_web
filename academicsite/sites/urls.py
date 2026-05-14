from django.urls import path, register_converter
from . import views, converters

register_converter(converters.FourDigitYearConverter, 'year')
register_converter(converters.TwoDigitMonthConverter, 'month')
register_converter(converters.PositiveIntConverter, 'posint')

urlpatterns = [
    # Основные страницы
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('material/<slug:material_slug>/', views.show_material, name='material'),
    path('methodology/', views.methodology, name='methodology'),
    path('for_teachers/', views.for_teachers, name='for_teachers'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    #path('post/<int:post_id>/', views.show_post, name='post'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
    path('add-page/', views.addpage, name='add_page'),

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
]

handler404 = 'sites.views.page_not_found'