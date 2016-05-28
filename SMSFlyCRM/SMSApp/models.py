from django.db import models

# Add recognized model option to django
# :seealso: https://djangosnippets.org/snippets/2687/
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('db_route',)


class Area(models.Model):
    """Describes the area where electors live"""
    area_id = models.IntegerField(unique=True)
    area_name = models.CharField(null=True, max_length=250)
    region_id = models.ForeignKey('Region', to_field='region_id', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_areas'


class Building(models.Model):
    """Describes the building"""
    building_id = models.IntegerField(unique=True)
    building_number = models.CharField(null=True, max_length=20)
    street_id = models.ForeignKey('Street', to_field='street_id', on_delete=models.DO_NOTHING)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_buildings'


class Region(models.Model):
    """Describes the region where electors live"""
    region_id = models.IntegerField(unique=True)
    region_name = models.CharField(max_length=250)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_regions'


class Locality(models.Model):
    """Describes the locality where electors live"""
    locality_id = models.IntegerField(unique=True)
    locality_name = models.CharField(max_length=56)
    area_id = models.ForeignKey('Area', to_field='area_id', on_delete=models.DO_NOTHING)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_localities'


class Street(models.Model):
    """Describes the area where electors live"""
    street_id = models.IntegerField(unique=True)
    street_name = models.CharField(max_length=500)
    locality_id = models.ForeignKey('Locality', to_field='locality_id', on_delete=models.DO_NOTHING)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_streets'


class Project(models.Model):
    """Describes the project in terms of which the elector is contacted"""
    project_id = models.IntegerField(unique=True)
    project_name = models.CharField(max_length=255)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_projects'


class ProjectContact(models.Model):
    """Describes the contacts in project"""
    contact_id = models.IntegerField(unique=True)
    area_name = models.CharField(max_length=255)
    project_id = models.ForeignKey('Project', to_field='project_id', on_delete=models.DO_NOTHING)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_project_contacts'


class FollowerContact(models.Model):
    """Describes the contact with elector"""
    id = models.IntegerField(unique=True, primary_key=True)
    contact_date = models.DateField(null=True)
    follower_id = models.ForeignKey('Follower', to_field='follower_id', on_delete=models.DO_NOTHING)
    contact_id = models.ForeignKey('ProjectContact', to_field='contact_id', on_delete=models.DO_NOTHING, null=True)
    follower_status_id = models.ForeignKey('FollowerStatus', to_field='follower_status_id', on_delete=models.DO_NOTHING,
                                           null=True)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_follower_contacts'


class Candidate(models.Model):
    """Describes the elections candidate"""
    candidate_id = models.IntegerField(unique=True)
    candidate_name = models.CharField(max_length=250)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_candidates'


class FollowerCandidate(models.Model):
    """Describes the relation between candidate and elector"""
    follower_id = models.IntegerField(unique=True)
    candidate_id = models.ForeignKey('Candidate', to_field='candidate_id', on_delete=models.DO_NOTHING)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_follower_candidates'


class PollPlace(models.Model):
    """Describes the poll location"""
    polplace_id = models.IntegerField(nunique=True)
    polplace_number = models.CharField(null=True, max_length=14)
    region_id = models.ForeignKey('Region', to_field='region_id', null=True, on_delete=models.DO_NOTHING)
    area_id = models.ForeignKey('Area', to_field='area_id', null=True,  on_delete=models.DO_NOTHING)
    locality_id = models.ForeignKey('Locality', to_field='locality_id', null=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_polplaces'


class FamilyStatus(models.Model):
    """Describes family status"""
    family_status_id = models.IntegerField(unique=True)
    family_status_name = models.CharField(null=True, max_length=250)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_family_status'


class Education(models.Model):
    """Describes elector's education"""
    education_id = models.IntegerField(unique=True)
    education_name = models.CharField(null=True, max_length=250)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_education'


class SocialCategory(models.Model):
    """Describes social category"""
    social_category_id = models.IntegerField(unique=True)
    social_category_name = models.CharField(null=True, max_length=255)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_social_category'


class Sex(models.Model):
    """Describes elector's gender"""
    sex_id = models.IntegerField(unique=True)
    sex_name = models.CharField(max_length=225)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_sex'


class FollowerStatus(models.Model):
    """Describes family status"""
    follower_status_id = models.IntegerField(unique=True)
    follower_status_name = models.CharField(max_length=255)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_follower_status'


class Follower(models.Model):
    """Describes candidate's follower"""
    follower_id = models.IntegerField(unique=True)
    lastname = models.CharField(null=True, max_length=255)
    firstname = models.CharField(null=True, max_length=255)
    middlename = models.CharField(null=True, max_length=255)
    sex_id = models.ForeignKey('Sex', to_field='sex_id', null=True,  on_delete=models.DO_NOTHING)
    datebirth = models.DateField(null=True)
    social_category_id = models.ForeignKey('SocialCategory', to_field='social_category_id', related_name='followers',
                                           on_delete=models.DO_NOTHING, null=True)
    family_status_id = models.ForeignKey('FamilyStatus', to_field='family_status_id', related_name='followers',
                                         on_delete=models.DO_NOTHING, null=True)
    education_id = models.ForeignKey('Education', related_name='followers', to_field='education_id',
                                     on_delete=models.DO_NOTHING, null=True)
    cellphone = models.CharField(null=True, max_length=255)
    address_region_id = models.ForeignKey('Region', to_field='region_id', related_name='living_followers',
                                          on_delete=models.DO_NOTHING, null=True)
    address_area_id = models.ForeignKey('Area', to_field='area_id', related_name='living_followers',
                                        on_delete=models.DO_NOTHING, null=True)
    address_locality_id = models.ForeignKey('Locality', to_field='locality_id', related_name='living_followers',
                                            on_delete=models.DO_NOTHING, null=True)
    address_street_id = models.ForeignKey('Street', to_field='street_id', related_name='living_followers',
                                          on_delete=models.DO_NOTHING, null=True)
    address_builing_id = models.ForeignKey('Building', to_field='building_id', related_name='living_followers',
                                           on_delete=models.DO_NOTHING, null=True)
    regaddress_region_id = models.ForeignKey('Region', to_field='region_id', related_name='registered_followers',
                                             on_delete=models.DO_NOTHING, null=True)
    regaddress_area_id = models.ForeignKey('Area', to_field='area_id', related_name='registered_followers',
                                           on_delete=models.DO_NOTHING, null=True)
    regaddress_locality_id = models.ForeignKey('Locality', to_field='locality_id', related_name='registered_followers',
                                               on_delete=models.DO_NOTHING, null=True)
    regaddress_street_id = models.ForeignKey('Street', to_field='street_id', related_name='registered_followers',
                                             on_delete=models.DO_NOTHING, null=True)
    regaddress_builing_id = models.ForeignKey('Building', to_field='building_id', related_name='registered_followers',
                                              on_delete=models.DO_NOTHING, null=True)
    polplace_id = models.ForeignKey('PollPlace', to_field='polplace_id', related_name='followers',
                                    on_delete=models.DO_NOTHING, null=True)
    last_contact_id = models.ForeignKey('FollowerContact', to_field='id', on_delete=models.DO_NOTHING, null=True)
    last_status_id = models.ForeignKey('FollowerStatus', to_field='follower_status_id', on_delete=models.DO_NOTHING,
                                       null=True)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'sms_view_family_status'


class Campaign(models.Model):
    task = models.ForeignKey('Task')
    code = models.CharField(max_length=20)
    datetime_sent = models.DateTimeField()
    state = models.CharField()

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

    alphaname = models.ForeignKey('Alphaname')
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    start_date = models.DateField()
    type = models.IntegerField(choices=TYPE_LIST)
    end_date = models.DateField()
    created_by_crm_user_id = models.IntegerField
    triggered_by = models.IntegerField(null=True, choices=TRIGGERS_LIST)
    target_filter = models.TextField()
    state = models.IntegerField(choices=STATE_LIST)

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
    status = models.IntegerField(choices=STATUS_LIST)

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

    crm_elector_id = models.ForeignKey('Follower', to_field='follower_id', on_delete=models.DO_NOTHING)
    phone_number = models.CharField(max_length=12)
    message_text = models.CharField(max_length=402)
    datetime_scheduled = models.DateTimeField()
    datetime_sent = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_LIST)
    campaign = models.ForeignKey('Campaign')

    class Meta:
        db_route = 'internal_app'
