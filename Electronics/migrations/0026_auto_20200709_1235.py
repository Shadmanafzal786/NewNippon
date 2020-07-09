# Generated by Django 3.0.6 on 2020-07-09 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics', '0025_auto_20200709_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptop',
            name='slug',
            field=models.SlugField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='mobile',
            name='slug',
            field=models.SlugField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='image_url',
            field=models.URLField(blank=True, default='None'),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='image_url',
            field=models.URLField(blank=True, default='None'),
        ),
    ]