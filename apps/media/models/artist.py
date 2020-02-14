from django.db.models import Model, CharField, TextField, ManyToManyField, ImageField
from apps.media.models.genre import Genre


class Artist(Model):
    stage_name = CharField(max_length=200)
    info = TextField(blank=True)
    photo = ImageField(default=None)
    genre = ManyToManyField(Genre, related_name='artists')

    def __str__(self):
        return self.stage_name
