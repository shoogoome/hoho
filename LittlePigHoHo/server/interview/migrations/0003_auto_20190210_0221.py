# Generated by Django 2.1.2 on 2019-02-10 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0002_registrationtemplate_using'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationtemplate',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='registrationtemplate',
            name='start_time',
        ),
    ]
