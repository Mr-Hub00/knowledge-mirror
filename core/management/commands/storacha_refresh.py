from django.core.management.base import BaseCommand
from storacha_tokens import start_token_refresher, refresh_now

class Command(BaseCommand):
    help = "Refresh Storacha bridge tokens now and ensure the background refresher is running."

    def handle(self, *args, **options):
        try:
            refresh_now()  # force a refresh immediately
            self.stdout.write(self.style.SUCCESS("Storacha tokens refreshed."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Refresh failed: {e}"))
            raise

        # Start the background refresher (no-op if already started)
        try:
            start_token_refresher()
            self.stdout.write("Background refresher running (or already running).")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Could not start refresher: {e}"))