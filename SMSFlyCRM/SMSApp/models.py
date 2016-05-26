from django.db import models


class Area(models.Model):
    """Describes the area where electors live"""
    area_id = models.IntegerField(null=False)
    area_name = models.CharField(null=False, max_length=250)
    region_id = models.ForeignKey('Region', to_field='region_id', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sms_view_areas'


class Building(models.Model):
    """Describes the building"""
    building_id = models.IntegerField(null=False)
    building_number = models.CharField(null=False, max_length=20)
    street_id = models.ForeignKey('Street', to_field='street_id', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sms_view_buildings'


class Region(models.Model):
    """Describes the region where electors live"""
    region_id = models.IntegerField(null=False)
    region_name = models.CharField(null=False, max_length=250)

    class Meta:
        managed = False
        db_table = 'sms_view_regions'


class Locality(models.Model):
    """Describes the locality where electors live"""
    locality_id = models.IntegerField(null=False)
    locality_name = models.CharField(null=False, max_length=56)
    area_id = models.ForeignKey('Area', to_field='area_id', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sms_view_localities'


class Street(models.Model):
    """Describes the area where electors live"""
    street_id = models.IntegerField(null=False)
    street_name = models.CharField(null=False, max_length=500)
    locality_id = models.ForeignKey('Locality', to_field='locality_id', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sms_view_streets'


class Project(models.Model):
    """Describes the project in terms of which the elector is contacted"""
    project_id = models.IntegerField(null=False)
    project_name = models.CharField(null=False, max_length=255)

    class Meta:
        managed = False
        db_table = 'sms_view_projects'


class ProjectContact(models.Model):
    """Describes the contacts in project"""
    contact_id = models.IntegerField(null=False)
    area_name = models.CharField(null=False, max_length=255)
    project_id = models.ForeignKey('Project', to_field='project_id', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sms_view_project_contacts'


class FollowerContact(models.Model):
    """Describes the contact with elector"""
    id = models.IntegerField(null=False)
    contact_date = models.DateField(null=False)
    follower_id = models.ForeignKey('Follower', to_field='follower_id', on_delete=models.DO_NOTHING)
    contact_id = models.ForeignKey('ProjectContact', to_field='contact_id', on_delete=models.DO_NOTHING)
    follower_status_id = models.ForeignKey('FollowerStatus', to_field='follower_status_id', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sms_view_follower_contacts'


class Candidate(models.Model):
    """Describes the elections candidate"""
    candidate_id = models.IntegerField(null=False)
    candidate_name = models.CharField(null=False, max_length=250)

    class Meta:
        managed = False
        db_table = 'sms_view_candidates'


class FollowerCandidate(models.Model):
    """Describes the relation between candidate and elector"""
    follower_id = models.IntegerField(null=False)
    candidate_id = models.ForeignKey('Candidate', null=False, to_field='candidate_id', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sms_view_follower_candidates'


class Polplace(models.Model):
    """Describes the poll location"""
    polplace_id = models.IntegerField(null=False)
    polplace_number = models.CharField(null=False, max_length=14)
    region_id = models.ForeignKey('Region', to_field='region_id', on_delete=models.DO_NOTHING)
    area_id = models.ForeignKey('Area', to_field='area_id', on_delete=models.DO_NOTHING)
    locality_id = models.ForeignKey('Locality', to_field='locality_id', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sms_view_polplaces'


class FamilyStatus(models.Model):
    """Describes family status"""
    family_status_id = models.IntegerField(null=False)
    family_status_name = models.CharField(null=False, max_length=250)

    class Meta:
        managed = False
        db_table = 'sms_view_family_status'


class Education(models.Model):
    """Describes elector's education"""
    education_id = models.IntegerField(null=False)
    education_name = models.CharField(null=False, max_length=250)

    class Meta:
        managed = False
        db_table = 'sms_view_education'


class SocialCategory(models.Model):
    """Describes social category"""
    social_category_id = models.IntegerField(null=False)
    social_category_name = models.CharField(null=False, max_length=255)

    class Meta:
        managed = False
        db_table = 'sms_view_social_category'


class Sex(models.Model):
    """Describes elector's gender"""
    sex_id = models.IntegerField(null=False)
    sex_name = models.CharField(null=False, max_length=225)

    class Meta:
        managed = False
        db_table = 'sms_view_sex'


class FollowerStatus(models.Model):
    """Describes family status"""
    follower_status_id = models.IntegerField(null=False)
    follower_status_name = models.CharField(null=False, max_length=255)

    class Meta:
        managed = False
        db_table = 'sms_view_follower_status'


class Follower(models.Model):
    """Describes candidate's follower"""
    follower_id = models.IntegerField(null=False)
    lastname = models.CharField(null=False, max_length=255)
    firstname = models.CharField(null=False, max_length=255)
    middlename = models.CharField(null=False, max_length=255)
    sex_id = models.ForeignKey('Sex', to_field='sex_id', on_delete=models.DO_NOTHING)
    datebirth = models.DateField(null=False)
    social_category_id = models.ForeignKey('SocialCategory', to_field='social_category_id', on_delete=models.DO_NOTHING)
    family_status_id = models.ForeignKey('FamilyStatus', to_field='family_status_id', on_delete=models.DO_NOTHING)
    education_id = models.ForeignKey('Education', to_field='education_id', on_delete=models.DO_NOTHING)
    cellphone = models.CharField(max_length=255)
    address_region_id = models.ForeignKey('Region', to_field='region_id', on_delete=models.DO_NOTHING)
    address_area_id = models.ForeignKey('Area', to_field='area_id', on_delete=models.DO_NOTHING)
    address_locality_id = models.ForeignKey('Locality', to_field='locality_id', on_delete=models.DO_NOTHING)
    address_street_id = models.ForeignKey('Street', to_field='street_id', on_delete=models.DO_NOTHING)
    address_builing_id = models.ForeignKey('Building', to_field='building_id', on_delete=models.DO_NOTHING)
    regaddress_region_id = models.ForeignKey('Region', to_field='region_id', on_delete=models.DO_NOTHING)
    regaddress_area_id = models.ForeignKey('Area', to_field='area_id', on_delete=models.DO_NOTHING)
    regaddress_locality_id = models.ForeignKey('Locality', to_field='locality_id', on_delete=models.DO_NOTHING)
    regaddress_street_id = models.ForeignKey('Street', to_field='street_id', on_delete=models.DO_NOTHING)
    regaddress_builing_id = models.ForeignKey('Building', to_field='building_id', on_delete=models.DO_NOTHING)
    polplace_id = models.ForeignKey('Polplace', to_field='polplace_id', on_delete=models.DO_NOTHING)
    last_contact_id = models.ForeignKey('FollowerContact', to_field='id', on_delete=models.DO_NOTHING)
    last_status_id = models.ForeignKey('FollowerStatus', to_field='follower_status_id', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sms_view_family_status'
