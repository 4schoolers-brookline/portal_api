# Generated by Django 3.2.4 on 2021-07-16 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0012_auto_20210623_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='subject',
            field=models.CharField(choices=[('Mathematics', 'Mathematics'), ('Computer Science', 'Computer Science'), ('English', 'English'), ('Chemistry', 'Chemistry'), ('Physics', 'Physics'), ('History', 'History'), ('Academic Advising', 'Academic Advising'), ('Compeetitive Math', 'Compeetitive Math'), ('Projects', 'Projects'), ('Essay Writing', 'Essay Writing')], default='Academic Advising', max_length=30),
        ),
        migrations.AlterField(
            model_name='submission',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]