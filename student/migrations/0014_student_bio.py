# Generated by Django 3.2.4 on 2021-06-22 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_auto_20210622_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='bio',
            field=models.CharField(blank=True, max_length=215, null=True),
        ),
    ]