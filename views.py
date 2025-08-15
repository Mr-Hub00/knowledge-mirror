from django.shortcuts import render
from django.utils import timezone
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.services.receipts import send_stamp_receipt, send_verification_notice
from django.conf import settings
from core.models import DocumentStamp
from core.api.utils import make_share_token
import requests

def home(request):
    return render(request, "base.html")

def some_view(request, stamp_id):
    from core.models import DocumentStamp
    stamp = DocumentStamp.objects.get(id=stamp_id)
    share_url = None
    if getattr(settings, "FEATURE_SHARE_STAMP", False):
        token = make_share_token(stamp.id)
        share_url = f"/api/v1/stamps/{stamp.id}/shared?token={token}"

    to_email = getattr(stamp.owner, "email", None) or None
    send_stamp_receipt(stamp, to_email, share_url)

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

from core.services.storacha import get_headers  # Add this import at the top or before the function

def storacha_list():
    headers, bridge_url = get_headers()
    r = requests.post(bridge_url, json={"cap": "upload/list"}, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()