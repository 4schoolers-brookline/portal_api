# Generated by Django 3.2.4 on 2021-06-08 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_student_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/profile_images'),
        ),
    ]