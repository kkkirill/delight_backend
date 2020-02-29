from django.db.models import CharField, Model


class Genre(Model):
    HH = 'Hip - Hop'
    REG = 'Reggae'
    POP = 'Pop'
    IND = 'Indie'
    ROCK = 'Rock'
    CLS = 'Classic'
    RdB = 'R & B'
    JAZZ = 'Jazz'
    GENRES = (
        (HH, 'Hip - Hop'),
        (REG, 'Reggae'),
        (POP, 'Pop'),
        (IND, 'Indie'),
        (ROCK, 'Rock'),
        (CLS, 'Classic'),
        (RdB, 'R & B'),
        (JAZZ, 'Jazz'),
    )
    name = CharField(choices=GENRES, max_length=20, unique=True)

    def __str__(self):
        return self.name
