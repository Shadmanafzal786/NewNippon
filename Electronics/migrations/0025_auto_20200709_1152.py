# Generated by Django 3.0.6 on 2020-07-09 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics', '0024_auto_20200709_1141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='laptop',
            old_name='url',
            new_name='image_url',
        ),
        migrations.RenameField(
            model_name='mobile',
            old_name='url',
            new_name='image_url',
        ),
    ]
