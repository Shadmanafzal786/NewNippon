# Generated by Django 3.0.6 on 2020-07-09 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics', '0026_auto_20200709_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptop',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=300),
        ),
    ]
