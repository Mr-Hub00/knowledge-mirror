from django.contrib import admin
from django.utils import timezone
from .models import DocumentStamp
from core.services.receipts import send_stamp_receipt, send_verification_notice

@admin.register(DocumentStamp)
class DocumentStampAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "verified", "timestamped_at")
    list_filter = ("verified",)
    actions = ("mark_verified", "resend_receipt")

    def mark_verified(self, request, queryset):
        updated = 0
        for stamp in queryset:
            if not stamp.verified:
                stamp.verified = True
                stamp.verified_at = timezone.now()
                stamp.save(update_fields=["verified", "verified_at"])
                send_verification_notice(stamp, getattr(stamp.owner, "email", None))
                updated += 1
        self.message_user(request, f"Verified {updated} stamp(s).")
    mark_verified.short_description = "Mark verified + email notice"

    def resend_receipt(self, request, queryset):
        for stamp in queryset:
            send_stamp_receipt(stamp, getattr(stamp.owner, "email", None), share_url=None)
        self.message_user(request, f"Resent {queryset.count()} receipt(s).")
    resend_receipt.short_description = "Resend receipt email(s)"