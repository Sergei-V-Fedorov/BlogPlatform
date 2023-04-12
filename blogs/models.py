from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Blog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='blogs', verbose_name=_('пользователь'))
    name = models.CharField(max_length=100, verbose_name=_('название блога'))
    tags = models.CharField(max_length=50, verbose_name=_('строка тегов'))

    class Meta:
        verbose_name = _('блог')
        verbose_name_plural = _('блоги')

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='entries',
                             verbose_name=_('блог'))
    title = models.CharField(max_length=255, verbose_name=_('заголовок'))
    body_text = models.TextField(verbose_name=_('содержание'))
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date', 'id']
        verbose_name = _('статья')
        verbose_name_plural = _('статьи')


class File(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='files',
                              verbose_name=_('статья'))
    file = models.ImageField(upload_to='files/', verbose_name=_('файл'))
    description = models.TextField(blank=True, verbose_name=_('описание'))

    class Meta:
        verbose_name = _('файл')
        verbose_name_plural = _('файлы')

    def __str__(self):
        return self.description
