# Generated by Django 3.2.4 on 2021-06-07 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20210603_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
