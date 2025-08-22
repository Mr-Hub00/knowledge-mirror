import os
import json
from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    help = "List uploads from Storacha bridge using current environment variables"

    def handle(self, *args, **options):
        bridge_url = os.getenv("STORACHA_BRIDGE_URL", "https://up.storacha.network/bridge")
        space_did = os.getenv("STORACHA_SPACE_DID")
        auth = os.getenv("STORACHA_AUTH")
        secret = os.getenv("STORACHA_SECRET")

        if not all([bridge_url, space_did, auth, secret]):
            self.stderr.write(self.style.ERROR("Missing one or more Storacha env vars."))
            return

        headers = {
            "Authorization": auth,
            "X-Auth-Secret": secret,
            "Content-Type": "application/json",
        }
        body = {
            "tasks": [
                ["upload/list", space_did, {}]
            ]
        }
        try:
            resp = requests.post(bridge_url, json=body, headers=headers, timeout=30)
            resp.raise_for_status()
            print(json.dumps(resp.json(), indent=2))
            self.stdout.write(self.style.SUCCESS("Storacha bridge list succeeded."))
        except Exception as e:
            print("Response content:", resp.content)  # Add this line
            self.stderr.write(self.style.ERROR(f"Storacha bridge list failed: {e}"))