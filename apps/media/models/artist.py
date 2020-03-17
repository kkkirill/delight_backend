from django.db.models import (
    CharField, ManyToManyField, Model, TextField, URLField)


class Artist(Model):
    stage_name = CharField(max_length=200)
    info = TextField(blank=True)
    photo = URLField(default='image.png')
    genres = ManyToManyField('Genre', related_name='artists')

    def __str__(self):
        return self.stage_name
