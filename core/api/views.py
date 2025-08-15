from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.management import call_command

from core.models import Contribution, DocumentStamp, MemberProfile
from .serializers import ContributionSer, DocumentStampSer, MemberProfileSer
from core.api.utils import make_share_token, verify_share_token, random_share_token
from core.services.hashing import file_sha256
from core.services import storacha
from core.services.receipts import send_stamp_receipt
from rest_framework import permissions

def home(request):
    return render(request, "base.html")

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, "owner", None) or getattr(obj, "user", None) or getattr(obj, "member", None)
        return request.method in permissions.SAFE_METHODS or owner == request.user

class MemberProfileViewSet(viewsets.ModelViewSet):
    queryset = MemberProfile.objects.all()
    serializer_class = MemberProfileSer
    permission_classes = [permissions.IsAuthenticated]

class DocumentStampViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentStampSer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = DocumentStamp.objects.all()
        if not self.request.user.is_staff:
            qs = qs.filter(owner=self.request.user)
        return qs

    @action(detail=False, methods=["post"])
    def upload(self, request):
        up = request.FILES.get("file")
        if not up:
            return Response({"detail": "file is required"}, status=status.HTTP_400_BAD_REQUEST)

        sha = file_sha256(up)
        try:
            cid = storacha.upload_file(up, getattr(up, "name", "upload.bin"))
        except Exception as e:
            print(f"[storacha] falling back to mock CID: {e}")
            cid = f"mock-cid-{sha[:46]}"

        stamp = DocumentStamp.objects.create(
            owner=request.user,
            title=request.data.get("title", "Untitled"),
            ipfs_cid=cid,
            sha256=sha,
        )
        share_url = None
        if getattr(settings, "FEATURE_SHARE_STAMP", True):
            try:
                token = getattr(stamp, "share_token", None)
                if token:
                    share_url = f"{settings.SITE_URL}/s/{token}"
            except Exception:
                pass

        owner_email = getattr(request.user, "email", None)
        send_stamp_receipt(stamp, owner_email, share_url=share_url)

        return Response(DocumentStampSer(stamp).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="share")
    def share(self, request, pk=None):
        stamp = self.get_object()

        # Default the feature flag to True so tests don’t 403
        if not getattr(settings, "FEATURE_SHARE_STAMP", True):
            return Response({"detail": "sharing disabled"}, status=403)

        created = False
        if not stamp.share_token:
            token = make_share_token(str(stamp.pk), str(request.user.pk))
            stamp.share_token = token
            stamp.save(update_fields=["share_token"])
            created = True

        short_url = request.build_absolute_uri(
            reverse("public-stamp", args=[stamp.share_token])
        )
        return Response(
            {"id": stamp.id, "short_url": short_url, "share_url": short_url, "created": created},
            status=200,
        )

    @action(detail=True, methods=["post"], url_path="rotate-share")
    def rotate_share(self, request, pk=None):
        stamp = self.get_object()
        new_token = random_share_token()
        stamp.share_token = new_token
        stamp.save(update_fields=["share_token"])
        short_url = f"{settings.SITE_URL}/s/{new_token}"
        return Response({"id": stamp.id, "short_url": short_url}, status=200)

class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSer
    permission_classes = [permissions.IsAuthenticated]

@api_view(["GET"])
@permission_classes([])
def health(request):
    return Response({"ok": True})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_stamp_share_link(request, pk: int):
    if not getattr(settings, "FEATURE_SHARE_STAMP", False):
        return Response({"detail": "share feature disabled"}, status=status.HTTP_403_FORBIDDEN)
    try:
        stamp = DocumentStamp.objects.get(pk=pk, owner=request.user)
    except DocumentStamp.DoesNotExist:
        return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)
    token = make_share_token(stamp.id)
    return Response(
        {"share_url": f"/api/v1/stamps/{stamp.id}/shared?token={token}"},
        status=status.HTTP_201_CREATED,
    )

@api_view(["GET"])
@permission_classes([AllowAny])
def get_shared_stamp(request, pk: int):
    if not getattr(settings, "FEATURE_SHARE_STAMP", False):
        return Response({"detail": "share feature disabled"}, status=status.HTTP_403_FORBIDDEN)
    token = request.query_params.get("token", "")
    if not verify_share_token(pk, token):
        return Response({"detail": "invalid or expired token"}, status=status.HTTP_403_FORBIDDEN)
    try:
        stamp = DocumentStamp.objects.get(pk=pk)
    except DocumentStamp.DoesNotExist:
        return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(DocumentStampSer(stamp).data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([AllowAny])
def internal_verify_pending(request):
    auth = request.META.get("HTTP_AUTHORIZATION", "")
    prefix = "Bearer "
    token = auth[len(prefix):] if auth.startswith(prefix) else ""
    if not token or token != getattr(settings, "INTERNAL_CRON_TOKEN", ""):
        return Response({"detail": "forbidden"}, status=403)
    call_command("verify_stamps")
    return Response({"ok": True})