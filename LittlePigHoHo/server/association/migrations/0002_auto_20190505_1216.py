# Generated by Django 2.1.2 on 2019-05-05 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='associationattendance',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='association.AssociationDepartment'),
        ),
        migrations.AlterField(
            model_name='association',
            name='config',
            field=models.TextField(default='{"version": 0, "interview_version_dict": {}, "number_of_leave": 2, "attendance_proportion": 0.3, "version_dict": {}, "interview_version": 0}'),
        ),
        migrations.AlterField(
            model_name='associationaccount',
            name='permissions',
            field=models.TextField(default='{"interview": false, "repository": false, "scheduling": false, "attendance": false, "appraising": false, "notice": false, "task": false}'),
        ),
    ]
