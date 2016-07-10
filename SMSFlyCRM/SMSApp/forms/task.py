from django import forms
from django.utils.translation import ugettext_lazy as _
from datetimewidget.widgets import DateTimeWidget, DateWidget


from ..models.crm import (
    ProjectContact, FollowerStatus, Follower,
    Candidate, Area, Building, Region, Locality, Street,
    Project, PollPlace, FamilyStatus, Education, SocialCategory, Sex,
)

from ..models.task import Task


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
        label=_('Start date'),
        input_formats=DATETIME_INPUTS,
        widget=DateTimeWidget(usel10n=False, options=dateTimeOptions,
                              bootstrap_version=3))

    def __init__(self, request, *args, **kwargs):
        self._request = request
        user_id = self.crm_user_id

        self._extmeta = getattr(self.__class__, 'ExtMeta')

        if callable(self._extmeta):
            self._extmeta = self._extmeta()

        super().__init__(*args, **kwargs)

        try:
            # Pre-populating filter fields with data extracted from JSON
            recipients_filter_json = kwargs['instance'].recipients_filter_json
            if not recipients_filter_json.get('to_everyone'):
                self.data = self.data.copy()
                for k, v in recipients_filter_json.items():
                    setattr(kwargs['instance'], 'y', v)
                    key = k[:-3] if k.endswith('_id') else k
                    self.data[key] = v
        except KeyError:
            pass

        self.initialize_filter_fields()

        self.initial['created_by_crm_user_id'] = user_id
        self.initial['type'] = 0
        self.initial['state'] = 0

        for field in self.fields.values():
            field.error_messages.update({
                'required': 'The field {fieldname} is required'.format(
                    fieldname=field.label)
            })

    def clean(self):
        cleaned_data = super().clean()
        FILTER_FIELDS = [
            'regaddress_region', 'regaddress_locality', 'regaddress_street', 'regaddress_building',
            'address_region', 'address_area', 'address_locality', 'address_street', 'address_building',
            'sex', 'family_status', 'education', 'social_category', 'poll_place', 'contact',
            'candidate', 'status',
        ]
        cleaned_data['recipients_filter_json'] = {
            'to_everyone': self.cleaned_data['to_everyone']
        }
        if not self.cleaned_data['to_everyone']:
            for field in ('age_from', 'age_to'):
                if cleaned_data[field]:
                    cleaned_data['recipients_filter_json'][field] = int(cleaned_data[field])
            for field in FILTER_FIELDS:
                if cleaned_data[field]:
                    cleaned_data['recipients_filter_json']['{}_id'.format(field)] = cleaned_data[field].pk
        return cleaned_data

    def save(self, commit=True):
        task = super().save(commit=False)

        task.recipients_filter_json = self.cleaned_data['recipients_filter_json']

        task.activate()

        return task

    def initialize_filter_fields(self):
        user_id = self.crm_user_id
        for fld in self._extmeta.FILTER_FIELDS:
            if 'get_queryset' in fld:
                fld['kwargs']['queryset'] = fld['get_queryset'](user_id)
            self.fields[fld['name']] = fld['field_class'](
                initial=self.data.get(fld['name']), required=False,
                **fld.get('kwargs', {}))

    @property
    def request(self):
        return self._request

    @property
    def crm_user_id(self):
        return self._request.session['crm_user_id']

    class Meta:
        model = Task
        fields = ['alphaname', 'title', 'message_text', 'start_datetime', 'type',
                  'created_by_crm_user_id', 'state']
        labels = {
            'alphaname': _('Alphaname'),
            'title': _('Template title'),
            'type': _('Type'),
            'message_text': _('Message text'),
            'created_by_crm_user_id': 'CRM User Id',

            'triggered_by': _('Mailing type'),
            'touch_project': _('Project'),
            'touch_status': _('Status'),
            'touch_contact': _('Contact'),
            'touch_candidate': _('Candidate'),
            'trigger_status': _('Status'),
        }

        widgets = {
            'created_by_crm_user_id': forms.HiddenInput(),
            'type': forms.HiddenInput(),
            'state': forms.HiddenInput(),
        }

    class ExtMeta:
        FILTER_FIELDS = (
            {
                'name': 'to_everyone',
                'field_class': forms.BooleanField,
                'kwargs': {
                    'label': _('Send to all electors'),
                },
            },
            {
                'name': 'age_from',
                'field_class': forms.IntegerField,
                'kwargs': {
                    'label': _('Age from'),
                    'min_value': 0,
                },
            },
            {
                'name': 'age_to',
                'field_class': forms.IntegerField,
                'kwargs': {
                    'label': _('Age to'),
                    'min_value': 0,
                },
            },
            {
                'name': 'regaddress_region',
                'field_class': forms.ModelChoiceField,
                'get_queryset': (lambda user_id:
                                 Region.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Region'),
                },
            },
            {
                'name': 'regaddress_area',
                'field_class': Follower.regaddress_area.field.formfield,
                'get_queryset': (lambda user_id:
                                 Area.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Area'),
                },
            },
            {
                'name': 'regaddress_locality',
                'field_class': Follower.regaddress_locality.field.formfield,
                'get_queryset': (lambda user_id:
                                 Locality.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Locality'),
                },
            },
            {
                'name': 'regaddress_street',
                'field_class': Follower.regaddress_street.field.formfield,
                'get_queryset': (lambda user_id:
                                 Street.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Street'),
                },
            },
            {
                'name': 'regaddress_building',
                'field_class': Follower.regaddress_building.field.formfield,
                'get_queryset': (lambda user_id:
                                 Building.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Building'),
                },
            },
            {
                'name': 'address_region',
                'field_class': forms.ModelChoiceField,
                'get_queryset': (lambda user_id:
                                 Region.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Region'),
                },
            },
            {
                'name': 'address_area',
                'field_class': Follower.address_area.field.formfield,
                'get_queryset': (lambda user_id:
                                 Area.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Area'),
                },
            },
            {
                'name': 'address_locality',
                'field_class': Follower.address_locality.field.formfield,
                'get_queryset': (lambda user_id:
                                 Locality.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Locality'),
                },
            },
            {
                'name': 'address_street',
                'field_class': Follower.address_street.field.formfield,
                'get_queryset': (lambda user_id:
                                 Street.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Street'),
                },
            },
            {
                'name': 'address_building',
                'field_class': Follower.address_building.field.formfield,
                'get_queryset': (lambda user_id:
                                 Building.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Building'),
                },
            },
            {
                'name': 'sex',
                'field_class': forms.ModelChoiceField,
                'get_queryset': (lambda user_id:
                                 Sex.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Gender'),
                },
            },
            {
                'name': 'family_status',
                'field_class': forms.ModelChoiceField,
                'get_queryset': (lambda user_id:
                                 FamilyStatus.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Family status'),
                },
            },
            {
                'name': 'education',
                'field_class': forms.ModelChoiceField,
                'get_queryset': (lambda user_id:
                                 Education.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Education'),
                },
            },
            {
                'name': 'social_category',
                'field_class': forms.ModelChoiceField,
                'get_queryset': (lambda user_id:
                                 SocialCategory.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Social Category'),
                },
            },
            {
                'name': 'poll_place',
                'field_class': forms.ModelChoiceField,
                'get_queryset': (lambda user_id:
                                 PollPlace.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Poll place'),
                },
            },
            {
                'name': 'contact',
                'field_class': forms.ModelChoiceField,
                'get_queryset': (lambda user_id:
                                 ProjectContact.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Contact'),
                },
            },
            {
                'name': 'candidate',
                'field_class': forms.ModelChoiceField,
                'get_queryset': (lambda user_id:
                                 Candidate.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Candidate'),
                },
            },
            {
                'name': 'status',
                'field_class': forms.ModelChoiceField,
                'get_queryset': (lambda user_id:
                                 FollowerStatus.objects.for_user(user_id).all()),
                'kwargs': {
                    'label': _('Status'),
                },
            },
        )


class OneTimeTaskForm(TaskForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.initial['type'] = 0


class RecurringTaskForm(TaskForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.initial['type'] = 1

    def clean(self):
        cleaned_data = super().clean()

        # Set datetime start into RRULE
        cleaned_data['recurrence_rule'].dtstart = cleaned_data['start_datetime']

        try:
            # Retrieve and set end date from RRULE
            cleaned_data['end_date'] = max(rr.until for rr in cleaned_data['recurrence_rule'].rrules).date()
        except TypeError:
            cleaned_data['end_date'] = None  # Endless

        return cleaned_data

    class Meta(TaskForm.Meta):
        fields = ['alphaname', 'title', 'message_text', 'start_datetime', 'type',
                  'state', 'created_by_crm_user_id', 'recurrence_rule',
                  ]


class EventDrivenTaskForm(TaskForm):
    TRIGGER_FIELDS_LIST = (
        'touch_project', 'touch_contact',
        'touch_status', 'touch_candidate',
        'trigger_status',
    )

    end_date = forms.DateField(
        label=_('End date'),
        input_formats=TaskForm.DATETIME_INPUTS,
        widget=DateWidget(usel10n=False,
                          options=TaskForm.dateOptions, bootstrap_version=3))

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        user_id = self.crm_user_id
        self.initial['type'] = 2

        self.fields['touch_project'] = forms.ModelChoiceField(
            queryset=Project.objects.for_user(user_id).all(), required=False, label='Проект')
        self.fields['touch_contact'] = forms.ModelChoiceField(
            queryset=ProjectContact.objects.for_user(user_id).all(), required=False, label='Контакт')
        self.fields['touch_status'] = forms.ModelChoiceField(
            queryset=FollowerStatus.objects.for_user(user_id).all(), required=False, label='Статус')
        self.fields['touch_candidate'] = forms.ModelChoiceField(
            queryset=Candidate.objects.for_user(user_id).all(), required=False, label='Кандидат')
        self.fields['trigger_status'] = forms.ModelChoiceField(
            queryset=FollowerStatus.objects.for_user(user_id).all(), required=False, label='Статус')

    def clean(self):
        cleaned_data = super().clean()

        for field_name in self.TRIGGER_FIELDS_LIST:
            try:
                cleaned_data['{}_id'.format(field_name)] = cleaned_data[field_name].pk
            except AttributeError:
                pass
            finally:
                del cleaned_data[field_name]

        return cleaned_data

    def save(self, commit=True):
        task = super().save(commit=False)

        for field_name in self.TRIGGER_FIELDS_LIST:
            attr_name = '{}_id'.format(field_name)
            try:
                setattr(task, attr_name, self.cleaned_data[attr_name])
            except KeyError:
                pass

        task.save(commit=commit)

        return task

    class Meta(TaskForm.Meta):
        model = Task
        fields = ['alphaname', 'title', 'message_text', 'start_datetime', 'type', 'end_date',
                  'triggered_by', 'touch_project', 'touch_status', 'touch_contact',
                  'touch_candidate', 'trigger_status', 'created_by_crm_user_id', 'state']
