# Generated by Django 3.2.4 on 2021-06-09 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0008_auto_20210609_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='account_type',
            field=models.CharField(blank=True, choices=[('student', 'student'), ('manager', 'manager'), ('employee', 'employee'), ('parent', 'parent')], max_length=20, null=True),
        ),
    ]