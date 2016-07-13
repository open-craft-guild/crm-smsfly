import json
from datetime import datetime, timedelta

from django.db import models

from django.utils.translation import ugettext_lazy as _

from recurrence.fields import RecurrenceField

from .crm import Follower
from .campaign import Campaign
from ..utils import calculate_price_for


class Task(models.Model):
    TYPE_LIST = (
        (0, 'one-time'),
        (1, 'recurring'),
        (2, 'event-driven'),
    )

    TRIGGERS_LIST = (
        ('onElectorBirthday', _('On elector\'s birthday')),
        ('onElectorAdded', _('On adding elector to the database')),
        ('onElectorTouched', _('Elector touched')),
        ('onElectorStatusChanged', _('On elector status change')),
    )

    STATE_LIST = (
        (0, 'active'),
        (1, 'paused'),
        (2, 'complete'),
    )

    created_by_crm_user_id = models.IntegerField()
    alphaname = models.ForeignKey('Alphaname')
    title = models.CharField(max_length=255)
    message_text = models.TextField(max_length=402)
    recipients_filter = models.TextField()
    state = models.IntegerField(choices=STATE_LIST)
    code = models.CharField(max_length=20)
    start_datetime = models.DateTimeField(default=datetime.now)
    type = models.IntegerField(choices=TYPE_LIST)
    end_date = models.DateField(null=True)
    recurrence_rule = RecurrenceField()
    triggered_by = models.CharField(null=True, max_length=22, choices=TRIGGERS_LIST)
    touch_project = models.ForeignKey('Project', to_field='project_id', on_delete=models.DO_NOTHING, null=True)
    touch_status = models.ForeignKey('FollowerStatus', to_field='follower_status_id', related_name='+',
                                     on_delete=models.DO_NOTHING, null=True)
    touch_contact = models.ForeignKey('ProjectContact', to_field='contact_id', on_delete=models.DO_NOTHING, null=True)
    touch_candidate = models.ForeignKey('Candidate', to_field='candidate_id', on_delete=models.DO_NOTHING, null=True)
    trigger_status = models.ForeignKey('FollowerStatus', to_field='follower_status_id', related_name='+',
                                       on_delete=models.DO_NOTHING, null=True)

    def activate(self, *args, **kwargs):
        if datetime.now().date() > (self.start_datetime.date()
                                    if self.type == 0
                                    else self.end_date):
            raise ValueError(_('Cannot activate an out-of-date task'))

        self.state = 0
        return self.save(*args, **kwargs)

    def archive(self, *args, **kwargs):
        self.end_date = datetime.now().date()
        self.state = 2
        return self.save(*args, **kwargs)

    def pause(self, *args, **kwargs):
        if self.end_date and datetime.now().date() > self.end_date:
            raise ValueError(_('Cannot pause an out-of-date task'))

        self.state = 1
        return self.save(*args, **kwargs)

    @staticmethod
    def get_recipients_queryset_by_filter(recipients_filter, user_id=None, prefetch=True):
        qs = Follower.objects

        if user_id:
            qs = qs.for_user(user_id)

        if recipients_filter:
            _filter = recipients_filter.copy()
            age_from = _filter.pop('age_from', None)
            age_to = _filter.pop('age_to', None)

            qs = qs.filter(**_filter)

            if age_from:
                qs = qs.filter(datebirth__lte=datetime.now().date() - timedelta(days=age_from*365))

            if age_to:
                qs = qs.filter(datebirth__gte=datetime.now().date()-timedelta(days=age_to*365))

            if prefetch:
                qs = qs.select_related(
                    'sex', 'social_category', 'family_status', 'education',
                    'address_region', 'address_area', 'address_locality',
                    'address_street', 'address_building',
                    'regaddress_region', 'regaddress_area', 'regaddress_locality',
                    'regaddress_street', 'regaddress_building',
                    'poll_place', 'contact', 'status',
                )

        return qs

    @classmethod
    def get_recipients_amount_by_filter(cls, recipients_filter, user_id=None):
        return cls.get_recipients_queryset_by_filter(recipients_filter, user_id=user_id, prefetch=False).count()

    @property
    def recipients_amount(self):
        return self.__class__.get_recipients_amount_by_filter(
            self.recipients_filter_json, user_id=self.created_by_crm_user_id)

    @property
    def recipients_queryset(self):
        return self.__class__.get_recipients_queryset_by_filter(
            self.recipients_filter_json, user_id=self.created_by_crm_user_id)

    @property
    def recipients_filter_json(self):
        try:
            _filter = json.loads(self.recipients_filter)
            raise AttributeError if _filter.pop('to_everyone') else KeyError
        except KeyError:
            return _filter
        except (json.decoder.JSONDecodeError, AttributeError):
            return {}

    @recipients_filter_json.setter
    def recipients_filter_json(self, value):
        self.recipients_filter = json.dumps(value)

    @recipients_filter_json.deleter
    def recipients_filter_json(self):
        self.recipients_filter = None

    @property
    def est_cost(self):
        return calculate_price_for(
            self.recipients_amount, len(self.message_text))

    @property
    def end_datetime(self):
        return datetime.combine(self.end_date, datetime.min.time())

    def get_last_time_sent(self):
        return self.campaigns.latest().datetime_sent

    @property
    def last_time_sent(self):
        try:
            return self.get_last_time_sent()
        except Campaign.DoesNotExist:
            return None

    def get_occurrences_between(self, dtstart, dtend):
        return self.recurrence_rule.between(dtstart=dtstart, end=dtend)

    def get_next_send_time(self):
        TASK_OUT_OF_DATE_ERROR = 'Task {task} is out of date'.format(task=self)

        now = datetime.now()

        if self.end_date and now.date() > self.end_date:
            raise ValueError(TASK_OUT_OF_DATE_ERROR)

        if self.type == 1:  # recurring
            return self.recurrence_rule.after(now)
        elif self.type == 2:  # event-driven
            raise ValueError(TASK_OUT_OF_DATE_ERROR)
        elif self.type == 0:  # one-time
            return now

    @property
    def next_send_time(self):
        try:
            return self.get_next_send_time()
        except ValueError:
            return None

    def __str__(self):
        return '{} ({}). {}'.format(self.title, self.alphaname, self.state)

    class Meta:
        db_route = 'internal_app'
