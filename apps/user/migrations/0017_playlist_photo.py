# Generated by Django 2.2.4 on 2020-05-11 10:29

import delight.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_auto_20200510_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='photo',
            field=models.URLField(default='d52s6jdjsch27.cloudfront.net/default/media_logo.png', validators=[delight.validators.CustomURLValidator]),
        ),
    ]
