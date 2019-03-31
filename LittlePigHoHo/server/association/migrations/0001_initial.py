# Generated by Django 2.1.2 on 2019-03-17 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('school', '0001_initial'),
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
                ('config', models.TextField(default='{}')),
                ('colony', models.BooleanField(default=False)),
                ('repository_size', models.BigIntegerField(default=2147483648)),
                ('choosing_code', models.CharField(blank=True, default='', max_length=15)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.School')),
            ],
            options={
                'verbose_name_plural': '协会表',
                'verbose_name': '协会',
            },
        ),
        migrations.CreateModel(
            name='AssociationAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default='', max_length=50)),
                ('role', models.PositiveSmallIntegerField(choices=[(0, '干事'), (1, '部长'), (2, '会长'), (4, 'TEACHER'), (99, '系统管理员')], default=0)),
                ('retire', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.Association')),
            ],
            options={
                'verbose_name_plural': '协会人事表',
                'verbose_name': '协会人事',
            },
        ),
        migrations.CreateModel(
            name='AssociationAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=64)),
                ('description', models.TextField(blank=True, default='')),
                ('place', models.CharField(blank=True, default='', max_length=64)),
                ('distance', models.FloatField(default=50.0)),
                ('start_time', models.FloatField(default=0.0)),
                ('end_time', models.FloatField(default=0.0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.Association')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='association.AssociationAccount')),
                ('manager', models.ManyToManyField(blank=True, related_name='attendance_manager', to='association.AssociationAccount')),
            ],
            options={
                'verbose_name_plural': '协会考勤表',
                'verbose_name': '协会考勤',
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
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.Association')),
                ('manager', models.ManyToManyField(blank=True, related_name='department_manager', to='account.Account')),
            ],
            options={
                'verbose_name_plural': '部门表',
                'verbose_name': '部门',
            },
        ),
        migrations.AddField(
            model_name='associationaccount',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='association.AssociationDepartment'),
        ),
    ]
