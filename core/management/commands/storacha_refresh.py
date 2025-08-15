from django.core.management.base import BaseCommand
from storacha_tokens import refresh_now, start_token_refresher

class Command(BaseCommand):
    help = "Refresh Storacha tokens and start the background refresher."

    def handle(self, *args, **options):
        ok = refresh_now()
        if ok:
            self.stdout.write(self.style.SUCCESS("Storacha tokens refreshed."))
        else:
            self.stdout.write(self.style.ERROR("Storacha token refresh failed."))

        start_token_refresher()
        self.stdout.write(self.style.SUCCESS("Background refresher running..."))