# Generated by Django 3.0.2 on 2021-06-23 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_alter_studentaccount_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentaccount',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='studentdeposit',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='studentlessonbill',
            name='coefficent',
            field=models.FloatField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='studentlessonbill',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
