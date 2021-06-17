from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('category/<str:slug>/', get_news_by_category, name='category'),
    path('tag/<str:slug>/', get_news_by_tag, name='tag'),
    path('news/<str:slug>/', get_select_news, name='news'),
    path('search/', get_search_news, name='search'),
]
