# Generated by Django 2.1.2 on 2019-04-05 05:25

import common.core.dao.time_stamp
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('association', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociationNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(default='')),
                ('start_time', models.FloatField(default=0.0)),
                ('end_time', models.FloatField(default=0.0)),
                ('create_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('update_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.Association')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.AssociationAccount')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='association.AssociationDepartment')),
            ],
            options={
                'verbose_name': '通知',
                'verbose_name_plural': '通知表',
            },
        ),
    ]
