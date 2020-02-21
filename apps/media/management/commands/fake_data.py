from django.core.management.base import BaseCommand
from apps.media.seed.factories import factories


class Command(BaseCommand):
    help = 'Fills database with randomly created data'

    def handle(self, *args, **options):
        factories.fill()
