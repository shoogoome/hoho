# Generated by Django 2.1.2 on 2019-03-17 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('association', '0001_initial'),
        ('interview', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Registration',
            new_name='InterviewRegistration',
        ),
        migrations.RenameModel(
            old_name='RegistrationTemplate',
            new_name='InterviewRegistrationTemplate',
        ),
    ]
