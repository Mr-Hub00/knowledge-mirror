from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from core.models import DocumentStamp  # Ensure 'core' is in INSTALLED_APPS in settings.py
from core.services.storacha import get_headers
import requests
import os
from django.http import JsonResponse

def home(request):
    return render(request, "base.html")

def some_view(request, stamp_id):
    stamp = DocumentStamp.objects.get(id=stamp_id)
    share_url = None
    if getattr(settings, "FEATURE_SHARE_STAMP", False):
        try:
            from core.api.utils import make_share_token
        except ImportError:
            def make_share_token(stamp_id):
                return "dummy-token"
        token = make_share_token(stamp.id)
        share_url = f"/api/v1/stamps/{stamp.id}/shared?token={token}"

    to_email = getattr(stamp.owner, "email", None) or None
    # send_stamp_receipt(stamp, to_email, share_url)
    return JsonResponse({"share_url": share_url})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_stamp(request, pk: int):
    try:
        stamp = DocumentStamp.objects.get(pk=pk)
    except DocumentStamp.DoesNotExist:
        return Response({"detail": "not found"}, status=404)
    if not (request.user.is_staff or stamp.owner_id == request.user.id):
        return Response({"detail": "forbidden"}, status=403)
    txid = request.data.get("txid", "")
    stamp.verified = True
    stamp.verified_at = timezone.now()
    stamp.verify_txid = txid[:120]
    stamp.save(update_fields=["verified", "verified_at", "verify_txid"])
    return Response({"detail": "verified"})

def storacha_list():
    headers, bridge_url = get_headers()
    r = requests.post(bridge_url, json={"cap": "upload/list"}, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def storacha_health(request):
    return JsonResponse({
        "space_did": os.environ.get("STORACHA_SPACE_DID", "MISSING"),
        "refresher": "started"
    })

def health(request):
    return JsonResponse({"status": "ok"})