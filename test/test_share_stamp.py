import io
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_share_link_happy_path(settings):
    settings.FEATURE_SHARE_STAMP = True
    user = User.objects.create_user("alice", password="x")
    c = APIClient()
    assert c.login(username="alice", password="x") is True

    f = io.BytesIO(b"hello iam hub")
    f.name = "hello.txt"
    up = c.post("/api/v1/stamps/upload/", {"title": "Share Me", "file": f})
    assert up.status_code == 201
    assert up.data["title"] == "Share Me"
    assert up.data["owner"] == user.id

    link = c.post(f"/api/v1/stamps/{up.data['id']}/share/")
    # Accept either 200 or 201 for flexibility
    assert link.status_code in (200, 201)
    share_url = link.json()["share_url"]

    # test anonymous access
    c.logout()
    anon_access = c.get(share_url)
    assert anon_access.status_code == 200
    assert anon_access.data["title"] == "Share Me"

    public = APIClient()
    resp = public.get(share_url)
    assert resp.status_code == 200