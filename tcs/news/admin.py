from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = NewsAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'category', 'created_at', 'is_published', 'get_photo',)
    list_display_links = ('id', 'title',)
    search_fields = ('title',)
    list_filter = ('category',)
    readonly_fields = ('created_at', 'get_photo',)
    fields = ('title', 'slug', 'category', 'tags', 'author', 'content', 'photo', 'get_photo', 'views', 'created_at',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src"{obj.photo.url}" width="50">')
        return 'no photo'

    get_photo.short_description = 'Фото'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Author, AuthorAdmin)
