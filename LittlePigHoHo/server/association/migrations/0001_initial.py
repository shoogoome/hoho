# Generated by Django 2.1.2 on 2019-04-05 05:25

import common.core.dao.time_stamp
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('short_name', models.CharField(db_index=True, default='', max_length=10)),
                ('logo', models.CharField(blank=True, default='', max_length=255)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('backlog', models.TextField(default='{"attendance": {}}')),
                ('config', models.TextField(default='{"attendance_proportion": 0.3, "interview_version_dict": {}, "version": 0, "interview_version": 0, "number_of_leave": 2, "version_dict": {}}')),
                ('colony', models.BooleanField(default=False)),
                ('repository_size', models.BigIntegerField(default=2147483648)),
                ('choosing_code', models.CharField(blank=True, default='', max_length=15)),
                ('create_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('update_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.School')),
            ],
            options={
                'verbose_name': '协会',
                'verbose_name_plural': '协会表',
            },
        ),
        migrations.CreateModel(
            name='AssociationAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default='', max_length=50)),
                ('role', models.PositiveSmallIntegerField(choices=[(0, '干事'), (1, '部长'), (2, '会长'), (99, '系统管理员')], default=0)),
                ('permissions', models.TextField(default='{"notice": false, "scheduling": false, "repository": false, "interview": false, "appraising": false, "task": false}')),
                ('retire', models.BooleanField(default=False)),
                ('create_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('update_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.Association')),
            ],
            options={
                'verbose_name': '协会人事',
                'verbose_name_plural': '协会人事表',
            },
        ),
        migrations.CreateModel(
            name='AssociationAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=64)),
                ('description', models.TextField(blank=True, default='')),
                ('place_x', models.FloatField(default=0.0)),
                ('place_y', models.FloatField(default=0.0)),
                ('distance', models.FloatField(default=50.0)),
                ('start_time', models.FloatField(default=0.0)),
                ('end_time', models.FloatField(default=0.0)),
                ('create_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('update_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.Association')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='association.AssociationAccount')),
            ],
            options={
                'verbose_name': '协会考勤',
                'verbose_name_plural': '协会考勤表',
            },
        ),
        migrations.CreateModel(
            name='AssociationDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=64)),
                ('short_name', models.CharField(db_index=True, default='', max_length=10)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('config', models.TextField(default='{}')),
                ('create_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('update_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.Association')),
                ('manager', models.ManyToManyField(blank=True, related_name='department_manager', to='association.AssociationAccount')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门表',
            },
        ),
        migrations.AddField(
            model_name='associationaccount',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='association.AssociationDepartment'),
        ),
    ]
