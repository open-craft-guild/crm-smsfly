import json
from datetime import date

from django import forms
from django.utils.translation import ugettext_lazy as _
from datetimewidget.widgets import DateTimeWidget


from .models import (Alphaname, Task, ProjectContact, FollowerStatus,
                     Candidate, Area, Building, Region, Locality, Street,
                     Project, PollPlace, FamilyStatus, Education, SocialCategory, Sex)


class AlphanameForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by_crm_user_id'] = forms.IntegerField(
            label='CRM User Id', initial=request.session['crm_user_id'],
            widget=forms.HiddenInput())
        self.fields['registration_date'] = forms.DateField(
            initial=date.today(), widget=forms.HiddenInput())
        self.fields['status'] = forms.IntegerField(
            initial=2, widget=forms.HiddenInput())

    class Meta:
        model = Alphaname
        fields = ['name', 'created_by_crm_user_id', 'registration_date', 'status']
        labels = {
            'name': _('Альфаимя'),
        }
        widgets = {
            'created_by_crm_user_id': forms.HiddenInput(),
            'registration_date': forms.HiddenInput()
        }

    class Media:
        js = ['js/bootstrap-datetimepicker.js']
        css = {
            'all': ('css/datetimepicker.css',)
            }


class TaskForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_id = request.session['crm_user_id']
        self.fields['created_by_crm_user_id'] = forms.IntegerField(
            label='CRM User Id', initial=user_id,
            widget=forms.HiddenInput())
        self.fields['type'].widget = forms.HiddenInput()
        self.initial['type'] = 0
        self.fields['state'].widget = forms.HiddenInput()
        self.initial['state'] = 0
        self.fields['recipients_filter'].widget = forms.HiddenInput()
        self.initial['recipients_filter'] = 0
        self.fields['to-everyone'] = forms.BooleanField(
            label=_('Отправить всем избирателям'), required=False)
        self.fields['age-from'] = forms.IntegerField(
            label=_('От'), min_value=0, required=False)
        self.fields['age-to'] = forms.IntegerField(
            label=_('До'), min_value=0, required=False)
        self.fields['reg-region'] = forms.ModelChoiceField(
            label=_('Область'), queryset=Region.objects.for_user(user_id).all(), required=False)
        self.fields['reg-area'] = forms.ModelChoiceField(
            label=_('Район'), queryset=Area.objects.for_user(user_id).all(), required=False)
        self.fields['reg-locality'] = forms.ModelChoiceField(
            label=_('Населенный пункт'), queryset=Locality.objects.for_user(user_id).all(),
            required=False)
        self.fields['reg-street'] = forms.ModelChoiceField(
            label=_('Улица'), queryset=Street.objects.for_user(user_id).all(), required=False)
        self.fields['reg-building'] = forms.ModelChoiceField(
            label=_('Дом'), queryset=Building.objects.for_user(user_id).all(), required=False)
        self.fields['actual-region'] = forms.ModelChoiceField(
            label=_('Область'), queryset=Region.objects.for_user(user_id).all(), required=False)
        self.fields['actual-area'] = forms.ModelChoiceField(
            label=_('Район'), queryset=Area.objects.for_user(user_id).all(), required=False)
        self.fields['actual-locality'] = forms.ModelChoiceField(
            label=_('Населенный пункт'), queryset=Locality.objects.for_user(user_id).all(),
            required=False)
        self.fields['actual-street'] = forms.ModelChoiceField(
            label=_('Улица'), queryset=Street.objects.for_user(user_id).all(), required=False)
        self.fields['actual-building'] = forms.ModelChoiceField(
            label=_('Дом'), queryset=Building.objects.for_user(user_id).all(), required=False)
        self.fields['sex'] = forms.ModelChoiceField(
            label=_('Пол'), queryset=Sex.objects.for_user(user_id).all(), required=False)
        self.fields['family-status'] = forms.ModelChoiceField(
            label=_('Семейное положение'), queryset=FamilyStatus.objects.for_user(user_id).all(),
            required=False)
        self.fields['education'] = forms.ModelChoiceField(
            label=_('Образование'), queryset=Education.objects.for_user(user_id).all(), required=False)
        self.fields['social-category'] = forms.ModelChoiceField(
            label=_('Социальная категория'), queryset=SocialCategory.objects.for_user(user_id).all(),
            required=False)
        self.fields['poll-place'] = forms.ModelChoiceField(
            label=_('Избирательный участок'), queryset=PollPlace.objects.for_user(user_id).all(),
            required=False)
        self.fields['contact'] = forms.ModelChoiceField(
            label=_('Контакт'), queryset=ProjectContact.objects.for_user(user_id).all(),
            required=False)
        self.fields['candidate'] = forms.ModelChoiceField(
            label=_('Кандидат'), queryset=Candidate.objects.for_user(user_id).all(),
            required=False)
        self.fields['status'] = forms.ModelChoiceField(
            label=_('Статус'), queryset=FollowerStatus.objects.for_user(user_id).all(), required=False)

    def save(self, commit=True):
        self.cleaned_data['type'] = 0
        self.cleaned_data['recipients_filter'] = json.dumps({
            'to-everyone': self.cleaned_data['to-everyone'],
            'age-from': self.cleaned_data['age-from'],
            'age-to': self.cleaned_data['age-to'],
            'reg-region': self.cleaned_data['reg-region'],
            'reg-locality': self.cleaned_data['reg-locality'],
            'reg-street': self.cleaned_data['reg-street'],
            'reg-building': self.cleaned_data['reg-building'],
            'actual-region': self.cleaned_data['actual-region'],
            'actual-area': self.cleaned_data['actual-area'],
            'actual-locality': self.cleaned_data['actual-locality'],
            'actual-street': self.cleaned_data['actual-street'],
            'actual-building': self.cleaned_data['actual-building'],
            'sex': self.cleaned_data['sex'],
            'family-status': self.cleaned_data['family-status'],
            'education': self.cleaned_data['education'],
            'social-category': self.cleaned_data['social-category'],
            'poll-place': self.cleaned_data['poll-place'],
            'contact': self.cleaned_data['contact'],
            'candidate': self.cleaned_data['candidate'],
            'status': self.cleaned_data['status']
        })
        return super().save(commit=commit)

    class Meta:
        model = Task
        fields = ['alphaname', 'title', 'message_text', 'start_datetime', 'recipients_filter', 'type',
                  'created_by_crm_user_id', 'state']
        labels = {
            'alphaname': _('Альфаимя'),
            'title': _('Название шаблона'),
            'message_text': _('Текст сообщения'),
            'start_datetime': _('Дата начала'),
        }

        dateTimeOptions = {
            'format': 'DD.MM.YYYY hh:mm'
        }

        widgets = {
            'start_datetime': DateTimeWidget(usel10n=True, options=dateTimeOptions, bootstrap_version=3),
            'state': forms.HiddenInput(),
        }


class OneTimeTaskForm(TaskForm):
    pass


class RecurringTaskForm(TaskForm):
    RECURRENCE_TYPES = (
        ('EVERY_WEEK', _('Каждую неделю')),
        ('EVERY_MONTH', _('Каждый месяц')),
        ('EVERY_YEAR', _('Каждый год')),
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['recurrence_rule'].widget = forms.HiddenInput()
        self.initial['recurrence_rule'] = ''
        self.fields['recurrence_type'] = forms.ChoiceField(
            choices=self.RECURRENCE_TYPES, label=_('Повторяется:'), required=True)

    def save(self, commit=True):
        form_data = super().save(commit=False)
        form_data.cleaned_data['recurrence_rule'] = json.dumps({
            'start_datetime': '11111',  # TODO: replace with fields
            'end_date': '11111',
            ####
            'type': form_data.cleaned_data['recurrence_type'],
            'period': 2,  # 2 yrs
            ###
            'type': 'EVERY_MONTH',
            'when': 'BY_MONTHDAY',  # BY_WEEKDAY
            'period': 2,  # 2 months
            ####
            'type': 'EVERY_WEEK',
            'days': [0, 3, 4],  # Sun, Wed, Thu
        })
        return form_data.save(commit=commit)

    class Meta:
        model = Task
        fields = ['alphaname', 'title', 'message_text', 'start_datetime', 'type', 'end_date',
                  'recurrence_rule', 'recipients_filter', 'state']
        labels = {
            'alphaname': _('Альфаимя'),
            'title': _('Название шаблона'),
            'message_text': _('Текст сообщения'),
            'start_date': _('Дата начала'),
            'type': _('Тип'),
            'end_date': _('Дата окончания'),
        }


class EventDrivenTaskForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_id = request.session['crm_user_id']
        self.fields['created_by_crm_user_id'] = forms.IntegerField(
            label='CRM User Id', initial=user_id, widgets=forms.HiddenInput())
        self.fields['touch_project'] = forms.ModelChoiceField(
            queryset=Project.objects.for_user(user_id).all())
        self.fields['touch_contact'] = forms.ModelChoiceField(
            queryset=ProjectContact.objects.for_user(user_id).all())
        self.fields['touch_status'] = forms.ModelChoiceField(
            queryset=FollowerStatus.objects.for_user(user_id).all())
        self.fields['touch_candidate'] = forms.ModelChoiceField(
            queryset=Candidate.objects.for_user(user_id).all())
        self.fields['trigger_status'] = forms.ModelChoiceField(
            queryset=FollowerStatus.objects.for_user(user_id).all())
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['recipients_filter'].widget = forms.HiddenInput()

    class Meta:
        model = Task
        fields = ['alphaname', 'title', 'message_text', 'start_datetime', 'type', 'end_date',
                  'touch_project', 'triggered_by', 'touch_status', 'touch_contact',
                  'touch_candidate', 'trigger_status', 'recipients_filter', ]
        labels = {
            'alphaname': _('Альфаимя'),
            'title': _('Название шаблона'),
            'message_text': _('Текст сообщения'),
            'start_datetime': _('Дата начала'),
            'type': _('Тип'),
            'end_date': _('Дата окончания'),
            'triggered_by': _('Тип даты отправки'),
            'touch_project': _('Проект'),
            'touch_status': _('Статус'),
            'touch_contact': _('Контакт'),
            'touch_candidate': _('Кандидат'),
            'trigger_status': _('Статус'),
        }
