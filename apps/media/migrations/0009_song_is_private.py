# Generated by Django 2.2.4 on 2020-05-10 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0008_remove_album_songs_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
