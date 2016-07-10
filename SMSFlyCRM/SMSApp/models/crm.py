from datetime import date

from django.db import models

from smart_selects.db_fields import ChainedForeignKey


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
        db_table = 'DIR_AREAS'


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
        db_table = 'DIR_BUILDINGS'


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
        db_table = 'DIR_LOCALITIES'
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
        db_table = 'DIR_STREETS'
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
        db_table = 'DB_PROJECTS'


class ProjectContact(models.Model):
    """Describes the contacts in project"""
    contact_id = models.IntegerField(unique=True, primary_key=True)
    contact_name = models.CharField(max_length=255)
    contact_project = models.ForeignKey('Project', to_field='project_id', on_delete=models.DO_NOTHING)

    objects = ExternalCRMManager()

    def __str__(self):
        return '{}'.format(self.contact_name)

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'DB_CONTACTS'
        # unique_together = ('contact_id', 'project_id')


class FollowerContact(models.Model):
    """Describes the contact with elector"""
    id = models.IntegerField(db_column='follower_contact_id', unique=True, primary_key=True)
    contact_date = models.DateField(db_column='follower_contact_date', null=True)
    follower = models.ForeignKey('Follower', to_field='follower_id', on_delete=models.DO_NOTHING)
    contact = models.ForeignKey('ProjectContact', to_field='contact_id',
                                db_column='FOLLOWER_CONTACT_PROJECT_CONTACT_ID',
                                on_delete=models.DO_NOTHING, null=True)
    follower_status = models.ForeignKey('FollowerStatus', to_field='follower_status_id', on_delete=models.DO_NOTHING,
                                        null=True, db_column='FOLLOWER_CONTACT_STATUS_ID')

    def __str__(self):
        return '{} {}, контакт {} {}'.format(self.follower.lastname, self.follower.firstname, self.contact_date,
                                             self.contact.contact_name)

    objects = ExternalCRMManager()

    class Meta:
        db_route = 'external_app'
        managed = False
        db_table = 'DB_FOLLOWER_CONTACTS'
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
        db_table = 'DIR_FAMILY_STATUSES'


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
        db_table = 'DIR_EDUCATIONS'


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
        db_table = 'DIR_SOCIAL_CATEGORIES'


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
        db_table = 'DIR_SEX'


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
        db_table = 'DIR_FOLLOWER_STATUS'


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
