# Generated by Django 3.2.4 on 2021-06-08 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_student_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
