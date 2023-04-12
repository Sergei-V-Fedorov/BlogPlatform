from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profiles',
                                verbose_name=_('пользователь'))
    registration_date = models.DateField(auto_now_add=True, verbose_name=_('дата регистрации'))
    avatar = models.ImageField(upload_to='files/', blank=True, verbose_name=_('аватар'))

    class Meta:
        verbose_name = _('профиль')
        verbose_name_plural = _('профили')

    def __str__(self):
        return f'Profile of {self.user}'
