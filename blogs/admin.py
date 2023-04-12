from django.contrib import admin
from .models import Blog, Entry, File


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'tags']


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'blog']


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'entry', 'description']
