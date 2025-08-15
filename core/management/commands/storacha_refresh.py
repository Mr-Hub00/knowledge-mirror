from django.core.management.base import BaseCommand
from core.storacha import refresh_now, start_token_refresher  # Make sure these imports are correct

class Command(BaseCommand):
    help = "Refresh Storacha tokens and start the background refresher."

    def handle(self, *args, **options):
        refresh_now()
        self.stdout.write(self.style.SUCCESS("Storacha tokens refreshed."))
        start_token_refresher()
        self.stdout.write(self.style.SUCCESS("Background refresher running..."))