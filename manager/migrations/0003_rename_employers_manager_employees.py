# Generated by Django 3.2.4 on 2021-07-29 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_request'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manager',
            old_name='employers',
            new_name='employees',
        ),
    ]