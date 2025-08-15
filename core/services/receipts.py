from datetime import datetime
import io
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import localtime

try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

def _build_pdf(stamp) -> bytes:
    if not REPORTLAB_AVAILABLE:
        return b""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=LETTER)
    text = c.beginText(72, 720)
    text.textLine("IAmHub Document Stamp Receipt")
    text.textLine("--------------------------------")
    text.textLine(f"Title: {stamp.title}")
    text.textLine(f"Owner ID: {getattr(stamp.owner, 'id', '')}")
    text.textLine(f"SHA-256: {stamp.sha256}")
    text.textLine(f"IPFS CID: {stamp.ipfs_cid}")
    text.textLine(f"Timestamped at: {stamp.timestamped_at.isoformat()}")
    if getattr(stamp, "verified", False):
        text.textLine(f"Verified: Yes ({getattr(stamp, 'verified_at', '')})")
    else:
        text.textLine("Verified: Pending")
    c.drawText(text)
    c.showPage()
    c.save()
    pdf = buf.getvalue()
    buf.close()
    return pdf

def _receipt_text(stamp, share_url: str | None = None) -> str:
    ts = localtime(stamp.timestamped_at).strftime("%Y-%m-%d %H:%M:%S %Z")
    lines = [
        "IAmHub Document Stamp Receipt",
        "----------------------------------------",
        f"Title:       {stamp.title}",
        f"Owner ID:    {stamp.owner_id}",
        f"Stamp ID:    {stamp.id}",
        f"SHA-256:     {stamp.sha256}",
        f"IPFS CID:    {stamp.ipfs_cid or '(pending)'}",
        f"Timestamp:   {ts}",
    ]
    if share_url:
        lines.append(f"Share Link:  {share_url}")
    lines.append("")
    lines.append("Keep this receipt to prove integrity and time of stamping.")
    return "\n".join(lines)

def _receipt_html(stamp, share_url: str | None = None) -> str:
    ts = localtime(stamp.timestamped_at).strftime("%Y-%m-%d %H:%M:%S %Z")
    share_row = f"<p><strong>Share Link:</strong> {share_url}</p>" if share_url else ""
    return f"""
    <h2>IAmHub Document Stamp Receipt</h2>
    <p><strong>Title:</strong> {stamp.title}</p>
    <p><strong>Owner ID:</strong> {stamp.owner_id}</p>
    <p><strong>Stamp ID:</strong> {stamp.id}</p>
    <p><strong>SHA-256:</strong> <code>{stamp.sha256}</code></p>
    <p><strong>IPFS CID:</strong> <code>{stamp.ipfs_cid or '(pending)'}</code></p>
    <p><strong>Timestamp:</strong> {ts}</p>
    {share_row}
    <hr/>
    <p>Keep this receipt to prove integrity and time of stamping.</p>
    """

def send_stamp_receipt(stamp, to_email: str | None, share_url: str | None = None) -> None:
    if not getattr(settings, "FEATURE_EMAIL_RECEIPTS", True):
        return
    if not to_email:
        return

    context = {
        "title": stamp.title,
        "owner_id": getattr(stamp.owner, "id", None),
        "sha256": stamp.sha256,
        "ipfs_cid": stamp.ipfs_cid,
        "timestamped_at": stamp.timestamped_at,
        "verified": getattr(stamp, "verified", False),
        "verified_at": getattr(stamp, "verified_at", None),
        "share_url": share_url,
        "site_url": getattr(settings, "SITE_URL", "http://127.0.0.1:8000"),
        "stamp_id": stamp.id,
    }

    subject = f"IAmHub receipt — '{stamp.title}'"
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@iamhub.net")

    html = render_to_string("email/stamp_receipt.html", context)
    text = render_to_string("email/stamp_receipt.txt", context)

    msg = EmailMultiAlternatives(subject, text, from_email, [to_email])
    msg.attach_alternative(html, "text/html")

    pdf = _build_pdf(stamp)
    if pdf:
        msg.attach(f"iamhub-receipt-{stamp.id}.pdf", pdf, "application/pdf")

    msg.send()

def send_verification_notice(stamp, to_email: str | None) -> None:
    if not getattr(settings, "FEATURE_EMAIL_RECEIPTS", True):
        return
    if not to_email:
        return

    context = {
        "title": stamp.title,
        "sha256": stamp.sha256,
        "ipfs_cid": stamp.ipfs_cid,
        "verified_at": getattr(stamp, "verified_at", None),
        "site_url": getattr(settings, "SITE_URL", "http://127.0.0.1:8000"),
        "stamp_id": stamp.id,
    }

    subject = f"IAmHub verification — '{stamp.title}'"
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@iamhub.net")
    html = render_to_string("email/stamp_verified.html", context)
    text = render_to_string("email/stamp_verified.txt", context)

    msg = EmailMultiAlternatives(subject, text, from_email, [to_email])
    msg.attach_alternative(html, "text/html")
    msg.send()

share_url = None
if getattr(settings, "FEATURE_SHARE_STAMP", True):
    # If you have a share token, build the URL here
    # share_url = f"{settings.SITE_URL}/api/v1/stamps/{stamp.id}/shared?token={token}"
    pass

# Example: create or fetch a 'stamp' object before using it
# stamp = ...  # Assign your stamp instance here

# Example: set owner_email if you have a request object available
# owner_email = getattr(request.user, "email", None)
# Uncomment the next line after defining 'stamp' and 'owner_email'
# send_stamp_receipt(stamp, owner_email, share_url=share_url)