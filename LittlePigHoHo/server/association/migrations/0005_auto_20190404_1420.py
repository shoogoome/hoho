# Generated by Django 2.1.2 on 2019-04-04 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0004_auto_20190404_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='config',
            field=models.TextField(default='{"interview_version": 0, "attendance_proportion": 0.3, "number_of_leave": 2, "version_dict": {}, "interview_version_dict": {}, "version": 0}'),
        ),
        migrations.AlterField(
            model_name='associationaccount',
            name='permissions',
            field=models.TextField(default='{"scheduling": false, "task": false, "appraising": false, "interview": false, "notice": false, "repository": false}'),
        ),
    ]
