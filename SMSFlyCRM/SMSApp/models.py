import datetime
import json

from django.db import models

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
        return self.get_queryset().extra(where=('{user_id} = (select @user := {user_id})'.
                                                format(user_id=crm_user_id), ))


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
    follower_id = models.IntegerField(unique=True, primary_key=True)
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
    sex = models.ForeignKey('Sex', to_field='sex_id', null=True, on_delete=models.DO_NOTHING)
    datebirth = models.DateField(null=True)
    social_category = models.ForeignKey('SocialCategory', to_field='social_category_id', related_name='followers',
                                        on_delete=models.DO_NOTHING, null=True)
    family_status = models.ForeignKey('FamilyStatus', to_field='family_status_id', related_name='followers',
                                      on_delete=models.DO_NOTHING, null=True)
    education = models.ForeignKey('Education', related_name='followers', to_field='education_id',
                                  on_delete=models.DO_NOTHING, null=True)
    cellphone = models.CharField(null=True, max_length=255)
    address_region = models.ForeignKey('Region', to_field='region_id', related_name='living_followers',
                                       on_delete=models.DO_NOTHING, null=True)
    address_area = models.ForeignKey('Area', to_field='area_id', related_name='living_followers',
                                     on_delete=models.DO_NOTHING, null=True)
    address_locality = models.ForeignKey('Locality', to_field='locality_id', related_name='living_followers',
                                         on_delete=models.DO_NOTHING, null=True)
    address_street = models.ForeignKey('Street', to_field='street_id', related_name='living_followers',
                                       on_delete=models.DO_NOTHING, null=True)
    address_builing = models.ForeignKey('Building', to_field='building_id', related_name='living_followers',
                                        on_delete=models.DO_NOTHING, null=True)
    regaddress_region = models.ForeignKey('Region', to_field='region_id', related_name='registered_followers',
                                          on_delete=models.DO_NOTHING, null=True)
    regaddress_area = models.ForeignKey('Area', to_field='area_id', related_name='registered_followers',
                                        on_delete=models.DO_NOTHING, null=True)
    regaddress_locality = models.ForeignKey('Locality', to_field='locality_id', related_name='registered_followers',
                                            on_delete=models.DO_NOTHING, null=True)
    regaddress_street = models.ForeignKey('Street', to_field='street_id', related_name='registered_followers',
                                          on_delete=models.DO_NOTHING, null=True)
    regaddress_builing = models.ForeignKey('Building', to_field='building_id', related_name='registered_followers',
                                           on_delete=models.DO_NOTHING, null=True)
    polplace = models.ForeignKey('PollPlace', to_field='polplace_id', related_name='followers',
                                 on_delete=models.DO_NOTHING, null=True)
    last_contact = models.ForeignKey('FollowerContact', to_field='id', on_delete=models.DO_NOTHING, null=True,
                                     related_name='last_contact')
    last_status = models.ForeignKey('FollowerStatus', to_field='follower_status_id', on_delete=models.DO_NOTHING,
                                    null=True)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{} {} {}'.format(self.lastname, self.firstname, self.middlename)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_family_status'


class Campaign(models.Model):
    task = models.ForeignKey('Task')
    code = models.CharField(max_length=20)
    datetime_sent = models.DateTimeField()
    state = models.TextField()
    smsfly_campaign_id = models.IntegerField(default=0, null=True)  # campaign id given by smsfly

    def __str__(self):
        return '{}, {}'.format(self.task.title, self.datetime_sent)

    class Meta:
        db_route = 'internal_app'


class Task(models.Model):
    TYPE_LIST = (
        (0, 'one-time'),
        (1, 'recurring'),
        (2, 'event-driven'),
    )

    TRIGGERS_LIST = (
        (0, 'onElectorBirthday'),
        (1, 'onElectorAdded'),
        (2, 'onElectorTouched'),
        (3, 'onElectorStatusChanged'),
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
    start_datetime = models.DateTimeField(default=datetime.datetime.now)
    type = models.IntegerField(choices=TYPE_LIST)
    end_date = models.DateField(null=True)
    recurrence_rule = models.TextField()
    triggered_by = models.IntegerField(null=True, choices=TRIGGERS_LIST)
    touch_project = models.ForeignKey('Project', to_field='project_id', on_delete=models.DO_NOTHING, null=True)
    touch_status = models.ForeignKey('FollowerStatus', to_field='follower_status_id', related_name='+',
                                     on_delete=models.DO_NOTHING, null=True)
    touch_contact = models.ForeignKey('ProjectContact', to_field='contact_id', on_delete=models.DO_NOTHING, null=True)
    touch_candidate = models.ForeignKey('Candidate', to_field='candidate_id', on_delete=models.DO_NOTHING, null=True)
    trigger_status = models.ForeignKey('FollowerStatus', to_field='follower_status_id', related_name='+',
                                       on_delete=models.DO_NOTHING, null=True)

    @property
    def recipients_filter_json(self):
        return json.loads(self.recipients_filter)

    @recipients_filter_json.setter
    def recipients_filter_json(self, value):
        self.recipients_filter = json.dumps(value)

    @recipients_filter_json.deleter
    def recipients_filter_json(self):
        self.recipients_filter = None

    @property
    def recurrence_rule_json(self):
        return json.loads(self.recurrence_rule)

    @recurrence_rule_json.setter
    def recurrence_rule_json(self, value):
        self.recurrence_rule = json.dumps(value)

    @recurrence_rule_json.deleter
    def recurrence_rule_json(self):
        self.recurrence_rule = None

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

    def __str__(self):
        return '{} ({}). Зарегистрировано {} пользователем {}'.format(
            self.name, self.status, self.registration_date, self.created_by_crm_user_id)

    @property
    def text_status(self):
        return self.STATUS_LIST[self.status]

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
    )

    crm_elector = models.ForeignKey('Follower', to_field='follower_id', on_delete=models.DO_NOTHING)
    phone_number = models.CharField(max_length=12)
    message_text = models.CharField(max_length=402)
    datetime_scheduled = models.DateTimeField()
    datetime_sent = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_LIST)
    campaign = models.ForeignKey('Campaign')

    def __str__(self):
        return '{} к {}  ({})'.format(self.message_text, self.phone_number, self.status[1])

    class Meta:
        db_route = 'internal_app'
