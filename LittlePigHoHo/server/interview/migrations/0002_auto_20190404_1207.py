# Generated by Django 2.1.2 on 2019-04-04 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interviewregistration',
            old_name='additional',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='interviewregistrationtemplate',
            old_name='additional',
            new_name='config',
        ),
        migrations.RemoveField(
            model_name='interviewregistration',
            name='eliminate',
        ),
        migrations.RemoveField(
            model_name='interviewregistrationtemplate',
            name='using',
        ),
        migrations.AddField(
            model_name='interviewregistration',
            name='version',
            field=models.IntegerField(default=0),
        ),
    ]
