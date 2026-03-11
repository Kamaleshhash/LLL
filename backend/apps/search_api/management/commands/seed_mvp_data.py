from django.core.management.base import BaseCommand

from apps.search_api.services import load_mock_data


class Command(BaseCommand):
    help = 'Load mock land + litigation data for MVP demos'

    def handle(self, *args, **options):
        load_mock_data()
        self.stdout.write(self.style.SUCCESS('Mock MVP data loaded successfully.'))
