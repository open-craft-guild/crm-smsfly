# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 00:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('area_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('area_name', models.CharField(max_length=250, null=True)),
            ],
            options={
                'db_table': 'sms_view_areas',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('building_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('building_number', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'sms_view_buildings',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('candidate_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('candidate_name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'sms_view_candidates',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('education_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('education_name', models.CharField(max_length=250, null=True)),
            ],
            options={
                'db_table': 'sms_view_education',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='FamilyStatus',
            fields=[
                ('family_status_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('family_status_name', models.CharField(max_length=250, null=True)),
            ],
            options={
                'db_table': 'sms_view_family_status',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('follower_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('lastname', models.CharField(max_length=255, null=True)),
                ('firstname', models.CharField(max_length=255, null=True)),
                ('middlename', models.CharField(max_length=255, null=True)),
                ('datebirth', models.DateField(null=True)),
                ('cellphone', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'sms_view_family_status',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='FollowerCandidate',
            fields=[
                ('follower_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'db_table': 'sms_view_follower_candidates',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='FollowerContact',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('contact_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'sms_view_follower_contacts',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='FollowerStatus',
            fields=[
                ('follower_status_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('follower_status_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'sms_view_follower_status',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('locality_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('locality_name', models.CharField(max_length=56)),
            ],
            options={
                'db_table': 'sms_view_localities',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='PollPlace',
            fields=[
                ('polplace_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('polplace_number', models.CharField(max_length=14, null=True)),
            ],
            options={
                'db_table': 'sms_view_polplaces',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('project_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'sms_view_projects',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='ProjectContact',
            fields=[
                ('contact_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('contact_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'sms_view_project_contacts',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('region_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('region_name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'sms_view_regions',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('sex_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('sex_name', models.CharField(max_length=225)),
            ],
            options={
                'db_table': 'sms_view_sex',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='SocialCategory',
            fields=[
                ('social_category_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('social_category_name', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'sms_view_social_category',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('street_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('street_name', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'sms_view_streets',
                'managed': False,
                'db_route': 'external_app',
            },
        ),
        migrations.CreateModel(
            name='Alphaname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=11)),
                ('status', models.IntegerField(choices=[(0, 'ACTIVE'), (1, 'BLOCKED'), (2, 'MODERATE'), (3, 'LIMITED')])),
                ('registration_date', models.DateField()),
                ('created_by_crm_user_id', models.IntegerField()),
            ],
            options={
                'db_route': 'internal_app',
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('datetime_sent', models.DateTimeField()),
                ('state', models.TextField()),
            ],
            options={
                'db_route': 'internal_app',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12)),
                ('message_text', models.CharField(max_length=402)),
                ('datetime_scheduled', models.DateTimeField()),
                ('datetime_sent', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'PENDING'), (1, 'SENT'), (2, 'DELIVERED'), (3, 'EXPIRED'), (4, 'UNDELIV'), (5, 'STOPED'), (6, 'ERROR'), (7, 'USERSTOPED'), (8, 'ALFANAMELIMITED'), (9, 'STOPFLAG'), (10, 'NEW')])),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SMSApp.Campaign')),
                ('crm_elector', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='SMSApp.Follower')),
            ],
            options={
                'db_route': 'internal_app',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by_crm_user_id', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('message_text', models.TextField(max_length=402)),
                ('recipients_filter', models.TextField()),
                ('state', models.IntegerField(choices=[(0, 'active'), (1, 'paused'), (2, 'complete')])),
                ('code', models.CharField(max_length=20)),
                ('start_date', models.DateField()),
                ('type', models.IntegerField(choices=[(0, 'one-time'), (1, 'recurring'), (2, 'event-driven')])),
                ('end_date', models.DateField()),
                ('recurrence_rule', models.TextField()),
                ('triggered_by', models.IntegerField(choices=[(0, 'onElectorBirthday'), (1, 'onElectorAdded'), (2, 'onElectorTouched'), (3, 'onElectorStatusChanged')], null=True)),
                ('alphaname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SMSApp.Alphaname')),
                ('touch_candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SMSApp.Candidate')),
                ('touch_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SMSApp.ProjectContact')),
                ('touch_project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SMSApp.Project')),
                ('touch_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='SMSApp.FollowerStatus')),
                ('trigger_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='SMSApp.FollowerStatus')),
            ],
            options={
                'db_route': 'internal_app',
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SMSApp.Task'),
        ),
    ]
