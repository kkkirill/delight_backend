from django.core.management.base import BaseCommand

from utils import factories


class Command(BaseCommand):
    help = 'Fills media-related database with randomly created data'

    def handle(self, *args, **options):
        factories.fill()
