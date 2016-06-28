import json
from datetime import datetime, date, timedelta

from django.db import models

from django.utils.translation import ugettext_lazy as _

from recurrence.fields import RecurrenceField
from smart_selects.db_fields import ChainedForeignKey

from .utils import calculate_price_for

# Add recognized model option to django
# :seealso: https://djangosnippets.org/snippets/2687/
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('db_route',)


class ExternalCRMManager(models.Manager):
    """Lets one query remote views on behalf of CRM user

    The inspiration has been gained from:
    :seealso: http://stackoverflow.com/a/28222392
    """

    def for_user(self, crm_user_id):
        """Hacks setting @user SQL variable needed for user-personalized queries"""
        assert isinstance(crm_user_id, int)
        qs = self.get_queryset()
        try:
            next(iter(qs.raw('set @user:={user_id}'.format(user_id=crm_user_id))))
        except TypeError:
            pass  # hack for pre-setting SQL variable before query
        return qs


class Area(models.Model):
    """Describes the area where electors live"""
    area_id = models.IntegerField(unique=True, primary_key=True)
    area_name = models.CharField(null=True, max_length=250)
    region = models.ForeignKey('Region', to_field='region_id', on_delete=models.DO_NOTHING, null=True)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.area_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_areas'


class Building(models.Model):
    """Describes the building"""
    building_id = models.IntegerField(unique=True, primary_key=True)
    building_number = models.CharField(null=True, max_length=20)
    street = models.ForeignKey('Street', to_field='street_id', on_delete=models.DO_NOTHING)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.building_number)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_buildings'


class Region(models.Model):
    """Describes the region where electors live"""
    region_id = models.IntegerField(unique=True, primary_key=True)
    region_name = models.CharField(max_length=250)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.region_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_regions'


class Locality(models.Model):
    """Describes the locality where electors live"""
    locality_id = models.IntegerField(unique=True, primary_key=True)
    locality_name = models.CharField(max_length=56)
    area = models.ForeignKey('Area', to_field='area_id', on_delete=models.DO_NOTHING)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.locality_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_localities'
        # unique_together = ('area_id', 'locality_id')


class Street(models.Model):
    """Describes the area where electors live"""
    street_id = models.IntegerField(unique=True, primary_key=True)
    street_name = models.CharField(max_length=500)
    locality = models.ForeignKey('Locality', to_field='locality_id', on_delete=models.DO_NOTHING)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.street_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_streets'
        # unique_together = ('street_id', 'locality_id')


class Project(models.Model):
    """Describes the project in terms of which the elector is contacted"""
    project_id = models.IntegerField(unique=True, primary_key=True)
    project_name = models.CharField(max_length=255)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.project_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_projects'


class ProjectContact(models.Model):
    """Describes the contacts in project"""
    contact_id = models.IntegerField(unique=True, primary_key=True)
    contact_name = models.CharField(max_length=255)
    project = models.ForeignKey('Project', to_field='project_id', on_delete=models.DO_NOTHING)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.contact_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_project_contacts'
        # unique_together = ('contact_id', 'project_id')


class FollowerContact(models.Model):
    """Describes the contact with elector"""
    id = models.IntegerField(unique=True, primary_key=True)
    contact_date = models.DateField(null=True)
    follower = models.ForeignKey('Follower', to_field='follower_id', on_delete=models.DO_NOTHING)
    contact = models.ForeignKey('ProjectContact', to_field='contact_id', on_delete=models.DO_NOTHING, null=True)
    follower_status = models.ForeignKey('FollowerStatus', to_field='follower_status_id', on_delete=models.DO_NOTHING,
                                        null=True)

    def __str__(self):
        return '{} {}, контакт {} {}'.format(self.follower.lastname, self.follower.firstname, self.contact_date,
                                             self.contact.contact_name)

    objects = ExternalCRMManager()

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_follower_contacts'
        # unique_together = ('id', 'contact_date', 'follower_id', 'contact_id')


class Candidate(models.Model):
    """Describes the elections candidate"""
    candidate_id = models.IntegerField(unique=True, primary_key=True)
    candidate_name = models.CharField(max_length=250)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.candidate_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_candidates'


class FollowerCandidate(models.Model):
    """Describes the relation between candidate and elector"""
    follower = models.ForeignKey('Follower', to_field='follower_id', on_delete=models.DO_NOTHING)
    candidate = models.ForeignKey('Candidate', to_field='candidate_id', on_delete=models.DO_NOTHING)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.candidate.candidate_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_follower_candidates'


class PollPlace(models.Model):
    """Describes the poll location"""
    polplace_id = models.IntegerField(unique=True, primary_key=True)
    polplace_number = models.CharField(null=True, max_length=14)
    region = models.ForeignKey('Region', to_field='region_id', null=True, on_delete=models.DO_NOTHING)
    area = models.ForeignKey('Area', to_field='area_id', null=True,  on_delete=models.DO_NOTHING)
    locality = models.ForeignKey('Locality', to_field='locality_id', null=True, on_delete=models.DO_NOTHING)

    objects = ExternalCRMManager()

    def __str__(self):
        return 'Участок {}'.format(self.polplace_number)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_polplaces'


class FamilyStatus(models.Model):
    """Describes family status"""
    family_status_id = models.IntegerField(unique=True, primary_key=True)
    family_status_name = models.CharField(null=True, max_length=250)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.family_status_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_family_status'


class Education(models.Model):
    """Describes elector's education"""
    education_id = models.IntegerField(unique=True, primary_key=True)
    education_name = models.CharField(null=True, max_length=250)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.education_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_education'


class SocialCategory(models.Model):
    """Describes social category"""
    social_category_id = models.IntegerField(unique=True, primary_key=True)
    social_category_name = models.CharField(null=True, max_length=255)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.social_category_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_social_category'


class Sex(models.Model):
    """Describes elector's gender"""
    sex_id = models.IntegerField(unique=True, primary_key=True)
    sex_name = models.CharField(max_length=225)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.sex_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_sex'


class FollowerStatus(models.Model):
    """Describes family status"""
    follower_status_id = models.IntegerField(unique=True, primary_key=True)
    follower_status_name = models.CharField(max_length=255)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.follower_status_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_follower_status'


class Follower(models.Model):
    """Describes candidate's follower"""
    follower_id = models.IntegerField(unique=True, primary_key=True)
    lastname = models.CharField(null=True, max_length=255)
    firstname = models.CharField(null=True, max_length=255)
    middlename = models.CharField(null=True, max_length=255)
    sex = models.ForeignKey(Sex, to_field='sex_id', null=True, on_delete=models.DO_NOTHING)
    datebirth = models.DateField(null=True)
    social_category = models.ForeignKey(SocialCategory, to_field='social_category_id', related_name='followers',
                                        on_delete=models.DO_NOTHING, null=True)
    family_status = models.ForeignKey(FamilyStatus, to_field='family_status_id', related_name='followers',
                                      on_delete=models.DO_NOTHING, null=True)
    education = models.ForeignKey(Education, related_name='followers', to_field='education_id',
                                  on_delete=models.DO_NOTHING, null=True)
    cellphone = models.CharField(null=True, max_length=255)
    address_region = models.ForeignKey(Region, to_field='region_id', related_name='living_followers',
                                       on_delete=models.DO_NOTHING, null=True)
    address_area = ChainedForeignKey(Area, related_name='living_followers', chained_field='address_region',
                                     chained_model_field='region', null=True)
    address_locality = ChainedForeignKey(Locality, related_name='living_followers', chained_field='address_area',
                                         chained_model_field='area', null=True)
    address_street = ChainedForeignKey(Street, related_name='living_followers', chained_field='address_locality',
                                       chained_model_field='locality', null=True)
    address_building = ChainedForeignKey(Building, related_name='living_followers', chained_field='address_street',
                                         chained_model_field='street', null=True)
    regaddress_region = models.ForeignKey(Region, to_field='region_id', related_name='registered_followers',
                                          on_delete=models.DO_NOTHING, null=True)
    regaddress_area = ChainedForeignKey(Area, related_name='registered_followers', chained_field='regaddress_region',
                                        chained_model_field='region', null=True)
    regaddress_locality = ChainedForeignKey(Locality, related_name='registered_followers',
                                            chained_field='regaddress_area',
                                            chained_model_field='area', null=True)
    regaddress_street = ChainedForeignKey(Street, related_name='registered_followers',
                                          chained_field='regaddress_locality',
                                          chained_model_field='locality', null=True)
    regaddress_building = ChainedForeignKey(Building, related_name='registered_followers',
                                            chained_field='regaddress_street',
                                            chained_model_field='street', null=True)
    poll_place = ChainedForeignKey(PollPlace, db_column='polplace_id', related_name='registered_followers',
                                   chained_field='regaddress_locality',
                                   chained_model_field='locality', null=True)
    candidate = models.ManyToManyField(Candidate, through=FollowerCandidate,
                                       related_name='followers')
    contact = models.ForeignKey(FollowerContact, db_column='last_contact_id', to_field='id',
                                on_delete=models.DO_NOTHING, null=True, related_name='last_contact')
    status = models.ForeignKey(FollowerStatus, db_column='last_status_id', to_field='follower_status_id',
                               on_delete=models.DO_NOTHING, null=True)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{} {} {}'.format(self.lastname, self.firstname, self.middlename)

    def address(self):
        return '{st}, {bld}'.format(st=self.address_street, bld=self.address_building)

    @property
    def name(self):
        return '{last} {first} {mid}'.format(last=self.lastname, first=self.firstname, mid=self.middlename)

    @property
    def regaddress_full(self):
        try:
            return '{reg}, {ar}, {loc}, {st}, {bld}'.format(
                reg=self.regaddress_region, ar=self.regaddress_area, loc=self.regaddress_locality,
                st=self.regaddress_street, bld=self.regaddress_building)
        except Region.DoesNotExist:
            return None

    @property
    def address_full(self):
        try:
            return '{reg}, {ar}, {loc}, {st}, {bld}'.format(
                reg=self.address_region, ar=self.address_area, loc=self.address_locality,
                st=self.address_street, bld=self.address_building)
        except Region.DoesNotExist:
            return None

    @property
    def age(self):
        born = self.datebirth
        today = date.today()
        try:
            return int((today - born).days / 365)
        except TypeError:
            return None

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_followers'


class Campaign(models.Model):
    task = models.ForeignKey('Task', related_name='campaigns')
    code = models.CharField(max_length=20)
    datetime_sent = models.DateTimeField()
    state = models.TextField()
    smsfly_campaign_id = models.IntegerField(default=0, null=True)  # campaign id given by smsfly

    def __str__(self):
        return '{}, {}'.format(self.task.title or _('Noname'), self.datetime_sent)

    class Meta:
        db_route = 'internal_app'
        get_latest_by = 'datetime_sent'


class Task(models.Model):
    TYPE_LIST = (
        (0, 'one-time'),
        (1, 'recurring'),
        (2, 'event-driven'),
    )

    TRIGGERS_LIST = (
        ('onElectorBirthday', _('День рождения избирателя')),
        ('onElectorAdded', _('Внесение анкеты избирателя в базу')),
        ('onElectorTouched', _('Внесение касания с избирателем в базу')),
        ('onElectorStatusChanged', _('Смена статуса избирателя')),
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

    def activate(self, commit=True):
        if datetime.now().date() > self.end_date:
            raise ValueError(_('Cannot activate an out-of-date task'))

        self.state = 0
        return self.save(commit=commit)

    def archive(self, commit=True):
        self.end_date = datetime.now().date()
        return self.save(commit=commit)

    def pause(self, commit=True):
        if self.type == 0:
            raise ValueError(_('Cannot pause a one-time task'))

        if datetime.now().date() > self.end_date:
            raise ValueError(_('Cannot pause an out-of-date task'))

        self.state = 1
        return self.save(commit=commit)

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
                    'polplace', 'last_contact', 'last_status',
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


class Alphaname(models.Model):
    STATUS_LIST = (
        (0, 'ACTIVE'),
        (1, 'BLOCKED'),
        (2, 'MODERATE'),
        (3, 'LIMITED'),
    )

    name = models.CharField(max_length=11)
    status = models.IntegerField(choices=STATUS_LIST, null=True)
    registration_date = models.DateField()
    created_by_crm_user_id = models.IntegerField()

    def change_status_to(self, status_text, commit=True):
        self.text_status = status_text
        return self.save(commit=commit)

    def __str__(self):
        return '{} ({}). Зарегистрировано {} пользователем {}'.format(
            self.name, self.status, self.registration_date, self.created_by_crm_user_id)

    @property
    def text_status(self):
        return self.get_status_display()

    @text_status.setter
    def text_status(self, status_text):
        self.status = self.status_id_by_text(status_text)

    def status_id_by_text(self, status_text):
        for i, t in self.STATUS_LIST:
            if t == status_text:
                return i

        raise KeyError

    class Meta:
        db_route = 'internal_app'


class Message(models.Model):
    STATUS_LIST = (
        (0, 'PENDING'),
        (1, 'SENT'),
        (2, 'DELIVERED'),
        (3, 'EXPIRED'),
        (4, 'UNDELIV'),
        (5, 'STOPED'),
        (6, 'ERROR'),
        (7, 'USERSTOPED'),
        (8, 'ALFANAMELIMITED'),
        (9, 'STOPFLAG'),
        (10, 'NEW'),
        (11, 'ACCEPTED'),
    )

    crm_elector = models.ForeignKey(Follower, to_field='follower_id',
                                    on_delete=models.DO_NOTHING, related_name='messages')
    phone_number = models.CharField(max_length=12)
    message_text = models.CharField(max_length=402)
    datetime_scheduled = models.DateTimeField()
    datetime_sent = models.DateTimeField(null=True)
    status = models.IntegerField(choices=STATUS_LIST)
    campaign = models.ForeignKey('Campaign')

    @property
    def msg_cost(self):
        return calculate_price_for(1, len(self.message_text))

    @property
    def status_text(self):
        return self.get_status_display()

    @status_text.setter
    def status_text(self, status_text):
        self.status = self.status_id_by_text(status_text)

    def status_id_by_text(self, status_text):
        for i, t in self.STATUS_LIST:
            if t == status_text:
                return i

        raise KeyError

    def __str__(self):
        return '{} к {}  ({})'.format(self.message_text, self.phone_number, self.status_text)

    class Meta:
        db_route = 'internal_app'
