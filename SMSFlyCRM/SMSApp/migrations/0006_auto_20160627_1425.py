# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-27 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SMSApp', '0005_auto_20160622_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='crm_elector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages', to='SMSApp.Follower'),
        ),
        migrations.AlterField(
            model_name='message',
            name='datetime_sent',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.IntegerField(choices=[(0, 'PENDING'), (1, 'SENT'), (2, 'DELIVERED'), (3, 'EXPIRED'), (4, 'UNDELIV'), (5, 'STOPED'), (6, 'ERROR'), (7, 'USERSTOPED'), (8, 'ALFANAMELIMITED'), (9, 'STOPFLAG'), (10, 'NEW'), (11, 'ACCEPTED')]),
        ),
    ]
