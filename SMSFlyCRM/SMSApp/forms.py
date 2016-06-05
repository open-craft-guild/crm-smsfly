import json
from datetime import date

from django import forms
from django.utils.translation import ugettext_lazy as _
from datetimewidget.widgets import DateTimeWidget, DateWidget


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
            'registration_date': forms.HiddenInput(),
        }

    class Media:
        js = ['js/bootstrap-datetimepicker.js']
        css = {
            'all': ('css/datetimepicker.css',)
            }


class TaskForm(forms.ModelForm):
    DATETIME_INPUTS = [
        '%d.%m.%Y %H:%M',       # '25.10.2006 14:30'
        '%d.%m.%Y',             # '25.10.2006'
        '%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
        '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
        '%Y-%m-%d',             # '2006-10-25'
        '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
        '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
        '%m/%d/%Y',             # '10/25/2006'
        '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
        '%m/%d/%y %H:%M',       # '10/25/06 14:30'
        '%m/%d/%y',             # '10/25/06'
    ]

    dateTimeOptions = {
        'format': 'dd.mm.yyyy hh:ii'
    }

    dateOptions = {
        'format': 'dd.mm.yyyy'
    }

    start_datetime = forms.DateTimeField(
        label=_('Дата начала'),
        input_formats=DATETIME_INPUTS,
        widget=DateTimeWidget(usel10n=False, options=dateTimeOptions,
                              bootstrap_version=3))

    end_date = forms.DateField(
        label=_('Дата окончания'),
        input_formats=DATETIME_INPUTS,
        widget=DateWidget(usel10n=False,
                          options=dateOptions, bootstrap_version=3))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_id = request.session['crm_user_id']

        self.initial['created_by_crm_user_id'] = user_id
        self.initial['type'] = 0
        self.initial['state'] = 0
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

        for field in self.fields.values():
            field.error_messages.update({
                'required': 'The field {fieldname} is required'.format(
                    fieldname=field.label)
            })

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['recipients_filter'] = json.dumps({
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
        return cleaned_data

    class Meta:
        model = Task
        fields = ['alphaname', 'title', 'message_text', 'start_datetime', 'recipients_filter', 'type',
                  'created_by_crm_user_id', 'state']
        labels = {
            'alphaname': _('Альфаимя'),
            'title': _('Название шаблона'),
            'type': _('Тип'),
            'message_text': _('Текст сообщения'),
            'created_by_crm_user_id': 'CRM User Id',

            'triggered_by': _('Тип даты отправки'),
            'touch_project': _('Проект'),
            'touch_status': _('Статус'),
            'touch_contact': _('Контакт'),
            'touch_candidate': _('Кандидат'),
            'trigger_status': _('Статус'),
        }

        widgets = {
            'created_by_crm_user_id': forms.HiddenInput(),
            'type': forms.HiddenInput(),
            'state': forms.HiddenInput(),
            'recurrence_rule': forms.HiddenInput(),

            'state': forms.HiddenInput(),
            'recipients_filter': forms.HiddenInput(),
        }


class OneTimeTaskForm(TaskForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.initial['type'] = 0


class RecurringTaskForm(TaskForm):
    RECURRENCE_TYPES = (
        ('EVERY_WEEK', _('Каждую неделю')),
        ('EVERY_MONTH', _('Каждый месяц')),
        ('EVERY_YEAR', _('Каждый год')),
    )

    WEEKDAYS = (
        ('mon', 'пн'),
        ('tue', 'вт'),
        ('wed', 'ср'),
        ('thu', 'чт'),
        ('fri', 'пт'),
        ('sat', 'сб'),
        ('sun', 'нд'),
    )

    RANGE30 = [(str(x), str(x)) for x in range(1, 31)]

    recurrence_type = forms.ChoiceField(
        choices=RECURRENCE_TYPES, label=_('Повторяется:'), required=True,
        widget=forms.RadioSelect)
    recurrence_period = forms.ChoiceField(
        choices=RANGE30, label=_('Интервал:'), required=True)
    recurrence_weekdays = forms.MultipleChoiceField(
        choices=WEEKDAYS, label=_('Дни повторения'), required=False,
        widget=forms.CheckboxSelectMultiple())

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.initial['type'] = 1
        self.fields['recurrence_rule'].required = False

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['recurrence_rule'] = json.dumps({
            'start_datetime': '11111',  # TODO: replace with fields
            'end_date': '11111',
            ####
            'type': self.cleaned_data['recurrence_type'],
            'period': self.cleaned_data['recurrence_period'],  # 2 yrs
            ###
            'type': 'EVERY_MONTH',
            'when': 'BY_MONTHDAY',  # BY_WEEKDAY
            'period': 2,  # 2 months
            ####
            'type': 'EVERY_WEEK',
            'days': self.cleaned_data['recurrence_weekdays']  # Sun, Wed, Thu
        })
        return cleaned_data

    class Meta(TaskForm.Meta):
        fields = ['alphaname', 'title', 'message_text', 'start_datetime', 'type', 'end_date',
                  'recurrence_rule', 'recipients_filter', 'state',
                  'created_by_crm_user_id', 'recurrence_type']


class EventDrivenTaskForm(TaskForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        user_id = request.session['crm_user_id']
        self.initial['type'] = 2

        self.fields['touch_project'] = forms.ModelChoiceField(
            queryset=Project.objects.for_user(user_id).all(), required=False)
        self.fields['touch_contact'] = forms.ModelChoiceField(
            queryset=ProjectContact.objects.for_user(user_id).all(), required=False)
        self.fields['touch_status'] = forms.ModelChoiceField(
            queryset=FollowerStatus.objects.for_user(user_id).all(), required=False)
        self.fields['touch_candidate'] = forms.ModelChoiceField(
            queryset=Candidate.objects.for_user(user_id).all(), required=False)
        self.fields['trigger_status'] = forms.ModelChoiceField(
            queryset=FollowerStatus.objects.for_user(user_id).all(), required=False)

    class Meta(TaskForm.Meta):
        model = Task
        fields = ['alphaname', 'title', 'message_text', 'start_datetime', 'type', 'end_date',
                  'triggered_by', 'touch_project', 'touch_status', 'touch_contact',
                  'touch_candidate', 'trigger_status', 'recipients_filter', 'created_by_crm_user_id', 'state']
