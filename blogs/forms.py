from django import forms
from .models import Entry
from django.utils.translation import gettext_lazy as _


class UploadEntryFile(forms.Form):
    file = forms.FileField(label=_('Выбрать файл '))


class EntryForm(forms.ModelForm):
    file = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            label=_('Файлы'), required=False)
    description = forms.CharField(label=_('Описание'), required=False,
                                  widget=forms.Textarea)

    class Meta:
        model = Entry
        fields = ['title', 'body_text', 'file', 'description']
