from django import forms
from .models import Alphaname, Task


class AlphanameForm(forms.ModelForm):
    class Meta:
        model = Alphaname
        fields = ['name', ]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['alphaname', 'title', 'code', 'start_date', 'type', 'end_date', 'triggered_by', 'target_filter']
