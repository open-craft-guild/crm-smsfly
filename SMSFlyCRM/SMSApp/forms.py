from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Alphaname, Task


class AlphanameForm(forms.ModelForm):
    class Meta:
        model = Alphaname
        fields = ['name', ]
        labels = {
            'name': _('Альфаимя'),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['alphaname', 'title', 'code', 'start_date', 'type', 'end_date', 'triggered_by']
