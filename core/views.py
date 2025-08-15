import os
from django.http import HttpResponse, JsonResponse

def home(request):
    return HttpResponse("IAmHub engine online — UI coming last.")

def storacha_health(request):
    return JsonResponse({
        "space_did": os.environ.get("STORACHA_SPACE_DID", "MISSING"),
        "refresher": "started"  # or update if you track actual state
    })