# Generated by Django 3.0.6 on 2020-06-06 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptop',
            name='reviews',
            field=models.ImageField(default=3, max_length=1, upload_to=''),
        ),
    ]
