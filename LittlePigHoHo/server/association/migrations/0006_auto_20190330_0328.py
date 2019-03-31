# Generated by Django 2.1.2 on 2019-03-30 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0005_auto_20190329_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='associationattendance',
            name='place',
        ),
        migrations.AddField(
            model_name='associationattendance',
            name='end_time',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='associationattendance',
            name='place_x',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='associationattendance',
            name='place_y',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='associationattendance',
            name='start_time',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='associationaccount',
            name='permissions',
            field=models.TextField(default='{"appraising": false, "scheduling": false, "task": false, "interview": false, "repository": false, "notice": false}'),
        ),
    ]