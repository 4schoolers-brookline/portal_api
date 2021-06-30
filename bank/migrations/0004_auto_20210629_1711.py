# Generated by Django 3.0.2 on 2021-06-29 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_auto_20210623_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentaccount',
            name='bills',
            field=models.ManyToManyField(blank=True, null=True, to='bank.StudentLessonBill'),
        ),
        migrations.AlterField(
            model_name='studentaccount',
            name='deposits',
            field=models.ManyToManyField(blank=True, null=True, to='bank.StudentDeposit'),
        ),
    ]