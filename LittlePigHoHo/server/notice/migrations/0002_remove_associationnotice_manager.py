# Generated by Django 2.1.2 on 2019-03-27 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='associationnotice',
            name='manager',
        ),
    ]
