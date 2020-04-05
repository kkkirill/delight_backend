from django.core.exceptions import ObjectDoesNotExist
from django_redis import get_redis_connection

from apps.celery.celery import app
from apps.celery.models import Event
from apps.media.models import Song
from apps.user.models import User


@app.task(name='aggregate_listen_info')
def aggregate_listen_info():
    redis = get_redis_connection('default')
    keys = redis.keys('*')
    values = (redis.smembers(k) for k in keys)
    items = tuple((key.decode(), map(bytes.decode, values)) for key, values in
                  zip(keys, values))

    for key, values in items:
        ids = key.split('-')[:-1]
        user = User.objects.get(pk=ids[0])
        song = Song.objects.get(pk=ids[1])
        numbers = ([int(num) for num in v.split('-')] for v in values)
        listen_duration = sum(abs(v[0] - v[1]) for v in numbers)
        pct = listen_duration / song.duration if song.duration else 0
        data = {
            'user': user,
            'song': song,
            'listen_percentage': round(pct, 2),
        }
        try:
            eve = Event.objects.get(user=user, song=song)
            eve.listen_percentage = data['listen_percentage']
            eve.save()
        except ObjectDoesNotExist:
            Event.objects.create(**data)

    redis.flushall()
