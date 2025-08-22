from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.utils.timezone import localtime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.models import DocumentStamp
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from django.template import TemplateDoesNotExist

@api_view(["GET"])
@permission_classes([AllowAny])  # <- public access
def public_stamp_view(request, token: str):
    """
    Serves JSON by default; if the client asks for HTML, render the receipt template.
    """
    try:
        stamp = DocumentStamp.objects.select_related("owner").get(share_token=token)
    except DocumentStamp.DoesNotExist:
        # DRF JSON 404 so API callers get a clear payload
        return Response({"detail": "Not found"}, status=404)

    # If the client prefers HTML, render the template
    accept = request.META.get("HTTP_ACCEPT", "")
    if "text/html" in accept:
        # Ensure your template includes the phrase "Document Receipt"
        # and expects a `stamp` context var.
        try:
            return render(request, "public_stamp.html", {"stamp": stamp, "request": request})
        except TemplateDoesNotExist:
            return render(request, "share/public_stamp.html", {"stamp": stamp, "request": request})

    # Otherwise return JSON
    return Response({
        "id": stamp.id,
        "title": stamp.title,
        "owner": getattr(stamp.owner, "username", None),
        "ipfs_cid": stamp.ipfs_cid,
        "sha256": stamp.sha256,
        "timestamped_at": localtime(stamp.timestamped_at).isoformat() if stamp.timestamped_at else None,
        "verified": getattr(stamp, "verified", False),
        "verified_at": localtime(stamp.verified_at).isoformat() if getattr(stamp, "verified_at", None) else None,
    })

def public_stamp_pdf(request, token: str):
    if not token:
        return HttpResponseBadRequest("Missing token")
    try:
        stamp = DocumentStamp.objects.select_related("owner").get(share_token=token)
    except DocumentStamp.DoesNotExist:
        return HttpResponseNotFound("Not found")
    if "application/json" in request.headers.get("Accept", ""):
        return JsonResponse({
            "id": stamp.id,
            "title": stamp.title,
            "owner": getattr(stamp.owner, "username", None),
            "ipfs_cid": stamp.ipfs_cid,
            "sha256": stamp.sha256,
            "timestamped_at": stamp.timestamped_at.isoformat() if stamp.timestamped_at else None,
            "verified": getattr(stamp, "verified", False),
            "verified_at": getattr(stamp, "verified_at", None).isoformat() if getattr(stamp, "verified_at", None) else None,
        })
    ctx = {
        "stamp": stamp,
        "owner_name": getattr(stamp.owner, "username", "member"),
    }
    resp = HttpResponse(content_type="application/pdf")
    filename = f"iamhub-receipt-{stamp.id}.pdf"
    resp["Content-Disposition"] = f'inline; filename="{filename}"'

    c = canvas.Canvas(resp, pagesize=LETTER)
    width, height = LETTER
    x = 1 * inch
    y = height - 1 * inch

    def line(label, value):
        nonlocal y
        c.setFont("Helvetica-Bold", 10); c.drawString(x, y, f"{label}:")
        c.setFont("Helvetica", 10); c.drawString(x + 140, y, value or "")
        y -= 16

    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "IAmHub Document Receipt")
    y -= 24

    line("Title", stamp.title or "")
    line("Owner", getattr(stamp.owner, "username", "member"))
    line("SHA-256", stamp.sha256 or "")
    line("IPFS CID", stamp.ipfs_cid or "Pending")
    line("Timestamp", localtime(stamp.timestamped_at).strftime("%Y-%m-%d %H:%M:%S %Z") if stamp.timestamped_at else "")
    line("Verified", "Yes" if getattr(stamp, "verified", False) else "No")
    if getattr(stamp, "verified_at", None):
        line("Verified At", localtime(stamp.verified_at).strftime("%Y-%m-%d %H:%M:%S %Z"))

    y -= 10
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(x, y, f"Share Token: {stamp.share_token or ''}")
    y -= 14
    c.drawString(x, y, "Keep this receipt for your records.")

    c.showPage()
    c.save()
    return resp