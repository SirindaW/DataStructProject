# Generated by Django 3.2.9 on 2021-12-04 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20211204_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='first_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='account',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]