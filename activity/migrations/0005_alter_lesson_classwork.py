# Generated by Django 3.2.4 on 2021-06-08 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_auto_20210608_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='classwork',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lesson_classwork', to='activity.submission'),
        ),
    ]
