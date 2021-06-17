from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=55)
    slug = models.SlugField(max_length=55, verbose_name='url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Author(models.Model):
    title = models.CharField(max_length=155)
    slug = models.SlugField(max_length=155, verbose_name='url', unique=True)
    content = models.TextField(blank=True, verbose_name='об авторе')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', verbose_name='фото автора', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('author', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['title']


class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)
    author = models.ForeignKey('Author', on_delete=models.PROTECT, default=1, related_name='author')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликованно')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True)
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='category')
    is_published = models.BooleanField(verbose_name='опубликовать?', default=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='news')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']
