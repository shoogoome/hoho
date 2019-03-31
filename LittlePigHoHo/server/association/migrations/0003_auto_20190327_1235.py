# Generated by Django 2.1.2 on 2019-03-27 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0002_auto_20190327_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='backlog',
            field=models.TextField(default='{"attendance": {}}'),
        ),
        migrations.AlterField(
            model_name='association',
            name='config',
            field=models.TextField(default='{}'),
        ),
        migrations.AlterField(
            model_name='associationaccount',
            name='permissions',
            field=models.TextField(default='{"interview": false, "task": false, "notice": false, "scheduling": false, "repository": false, "appraising": false}'),
        ),
    ]