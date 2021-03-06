# Generated by Django 3.2.4 on 2021-06-22 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_student_exams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='student',
            name='exams',
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=215, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('percentage', models.IntegerField(blank=True, null=True)),
                ('taker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
    ]
