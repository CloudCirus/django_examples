from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import *
from django.db.models import F

categories = Category.objects.all()
general_context_data = {
    'categories': categories,
    'register': 'Регистрация',
    'login': 'вход',
}


def index(request):
    """главная страница - все новости"""
    #  queryset
    news = News.objects.all()
    #  последняя новость для отображения на странице - большим блоком
    # sort = []
    # for i in news:
    #     if i.is_published:
    #         sort.append(i)
    # last_news = sort[0]
    #  пагинация:
    page_num = request.GET.get('page', 1)
    number_of_news = 8  # кол-во отображаемых новостей
    # if int(page_num) == 1:
    #     number_of_news += 1  # на главной странице крупно выводим +1 новость - последнюю
    paginator = Paginator(news, number_of_news)
    page_objects = paginator.get_page(page_num)

    context = {
        **general_context_data,
        'news': news,
        # 'last_news': last_news,
        'page_obj': page_objects,
        'title': 'Главная'
    }
    return render(request, template_name='news/index.html', context=context)


def get_news_by_category(request, slug):
    """новости по категории"""
    #  queryset
    news = News.objects.filter(category__slug=slug)
    category = get_object_or_404(Category, slug=slug)
    # пагинация
    number_of_news = 8
    paginator = Paginator(news, number_of_news)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    context = {
        **general_context_data,
        'news': news,
        'page_obj': page_objects,
        'title': category.title
    }
    return render(request, template_name='news/category.html', context=context)


def get_news_by_tag(request, slug):
    """новости по тегу"""
    #  queryset
    news = News.objects.filter(tags__slug=slug)
    # пагинация
    number_of_news = 8
    paginator = Paginator(news, number_of_news)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    context = {
        **general_context_data,
        'news': news,
        'page_obj': page_objects,
    }
    return render(request, template_name='news/index.html', context=context)


def get_select_news(request, slug):
    """выбранная нонвость"""
    #  queryset
    news = get_object_or_404(News, slug=slug)
    #  для отображения популярных новостей в sidebar
    number_of_news = 5
    news_for_sidebar = News.objects.order_by('-views')[:number_of_news]
    #  вывод облака тегов
    tags_for_sidebar = Tag.objects.all()
    #  счетчик при просмотре
    views = News.objects.filter(slug=slug)
    views.update(views=F('views') + 1)

    context = {
        **general_context_data,
        'news': news,
        'news_for_sidebar': news_for_sidebar,
        'tags_for_sidebar': tags_for_sidebar,
        'title': news.title
    }
    return render(request, template_name='news/view_news.html', context=context)


def get_search_news(request):
    """поиск новостей"""
    #  queryset
    news = News.objects.filter(title__icontains=request.GET.get('s'))
    # пагинация
    number_of_news = 8
    paginator = Paginator(news, number_of_news)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    context = {
        'page_obj': page_objects,
        's': f"s={request.GET.get('s')}&"
    }
    return render(request, template_name='news/index.html', context=context)
