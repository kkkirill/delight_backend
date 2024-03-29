# Generated by Django 2.2.4 on 2020-05-12 21:16

import delight.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0009_song_is_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='photo',
            field=models.URLField(default='https://d52s6jdjsch27.cloudfront.net/default/media_logo.png', validators=[delight.validators.CustomURLValidator]),
        ),
        migrations.AlterField(
            model_name='artist',
            name='photo',
            field=models.URLField(default='https://d52s6jdjsch27.cloudfront.net/default/user_logo.png', validators=[delight.validators.CustomURLValidator]),
        ),
        migrations.AlterField(
            model_name='song',
            name='image',
            field=models.URLField(default='https://d52s6jdjsch27.cloudfront.net/default/media_logo.png', validators=[delight.validators.CustomURLValidator]),
        ),
    ]
