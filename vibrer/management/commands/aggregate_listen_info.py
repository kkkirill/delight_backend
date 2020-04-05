from django.core.management import BaseCommand

from vibrer.apps.celery.tasks import aggregate_listen_info


class Command(BaseCommand):
    help = 'Aggregate and save listens information into a database'

    def handle(self, *args, **options):
        aggregate_listen_info.delay()
