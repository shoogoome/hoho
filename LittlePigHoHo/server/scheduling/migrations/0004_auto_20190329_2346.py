# Generated by Django 2.1.2 on 2019-03-29 23:46

import common.core.dao.time_stamp
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0003_auto_20190329_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='associationaccountcurriculum',
            name='create_time',
            field=common.core.dao.time_stamp.TimeStampField(default=0),
        ),
        migrations.AlterField(
            model_name='associationaccountcurriculum',
            name='update_time',
            field=common.core.dao.time_stamp.TimeStampField(default=0),
        ),
        migrations.AlterField(
            model_name='associationcurriculum',
            name='create_time',
            field=common.core.dao.time_stamp.TimeStampField(default=0),
        ),
        migrations.AlterField(
            model_name='associationcurriculum',
            name='update_time',
            field=common.core.dao.time_stamp.TimeStampField(default=0),
        ),
        migrations.AlterField(
            model_name='associationscheduling',
            name='create_time',
            field=common.core.dao.time_stamp.TimeStampField(default=0),
        ),
        migrations.AlterField(
            model_name='associationscheduling',
            name='update_time',
            field=common.core.dao.time_stamp.TimeStampField(default=0),
        ),
    ]