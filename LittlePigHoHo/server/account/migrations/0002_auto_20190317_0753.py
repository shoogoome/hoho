# Generated by Django 2.1.2 on 2019-03-17 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.CharField(blank=True, default='', max_length=125),
        ),
    ]
