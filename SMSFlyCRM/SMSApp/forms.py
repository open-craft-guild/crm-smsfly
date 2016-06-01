import json

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import (Alphaname, Task, ProjectContact, FollowerStatus,
                     Candidate, Area, Building, Region, Locality, Street,
                     Project, PollPlace, FamilyStatus, Education, SocialCategory, Sex)


class AlphanameForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by_crm_user_id'] = forms.IntegerField(
            label='CRM User Id', initial=request.session['crm_user_id'],
            widgets=forms.HiddenInput())

    class Meta:
        model = Alphaname
        fields = ['name', 'created_by_crm_user_id']
        labels = {
            'name': _('Альфаимя'),
        }


class TaskForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_id = request.session['crm_user_id']
        self.fields['created_by_crm_user_id'] = forms.IntegerField(
            label='CRM User Id', initial=user_id,
            widget=forms.HiddenInput())
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['recipients_filter'].widget = forms.HiddenInput()
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
        form_model = super().save(commit=False)
        form_model.fields['type'] = 0
        self.fields['recipients_filter'] = json.dumps({
            'to-everyone': self.fields['to-everyone'],
            'age-from': self.fields['age-from'],
            'age-to': self.fields['age-to'],
            'reg-region': self.fields['reg-region'],
            'reg-locality': self.fields['reg-locality'],
            'reg-street': self.fields['reg-street'],
            'reg-building': self.fields['reg-building'],
            'actual-region': self.fields['actual-region'],
            'actual-area': self.fields['actual-area'],
            'actual-locality': self.fields['actual-locality'],
            'actual-street': self.fields['actual-street'],
            'actual-building': self.fields['actual-building'],
            'sex': self.fields['sex'],
            'family-status': self.fields['family-status'],
            'education': self.fields['education'],
            'social-category': self.fields['social-category'],
            'poll-place': self.fields['poll-place'],
            'contact': self.fields['contact'],
            'candidate': self.fields['candidate'],
            'status': self.fields['status']
        })
        if commit:
            form_model.save()
        return form_model

    class Meta:
        model = Task
        fields = ['alphaname', 'title', 'message_text', 'start_date', 'recipients_filter', 'type']
        labels = {
            'alphaname': _('Альфаимя'),
            'title': _('Название шаблона'),
            'message_text': _('Текст сообщения'),
            'start_date': _('Дата начала'),
        }


class OneTimeTaskForm(TaskForm):
    pass


class RecurringTaskForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['recipients_filter'].widget = forms.HiddenInput()
        self.fields['recurrence_rule'].widget = forms.HiddenInput()

    def save(self, commit=True):
        form_model = super().save(commit=False)
        form_model.fields['recurrence_rule'] = json.dumps({
            'start_date': '11111',  # TODO: replace with fields
            'end_date': '11111',
            ####
            'type': 'EVERY_YEAR',
            'period': 2,  # 2 yrs
            ###
            'type': 'EVERY_MONTH',
            'when': 'BY_MONTHDAY',  # BY_WEEKDAY
            'period': 2,  # 2 months
            ####
            'type': 'EVERY_WEEK',
            'days': [0, 3, 4],  # Sun, Wed, Thu
        })
        if commit:
            form_model.save()
        return form_model

    class Meta:
        model = Task
        fields = ['alphaname', 'title', 'message_text', 'start_date', 'type', 'end_date',
                  'recurrence_rule', 'recipients_filter', ]
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
        fields = ['alphaname', 'title', 'message_text', 'start_date', 'type', 'end_date',
                  'touch_project', 'triggered_by', 'touch_status', 'touch_contact',
                  'touch_candidate', 'trigger_status', 'recipients_filter', ]
        labels = {
            'alphaname': _('Альфаимя'),
            'title': _('Название шаблона'),
            'message_text': _('Текст сообщения'),
            'start_date': _('Дата начала'),
            'type': _('Тип'),
            'end_date': _('Дата окончания'),
            'triggered_by': _('Тип даты отправки'),
            'touch_project': _('Проект'),
            'touch_status': _('Статус'),
            'touch_contact': _('Контакт'),
            'touch_candidate': _('Кандидат'),
            'trigger_status': _('Статус'),
        }
