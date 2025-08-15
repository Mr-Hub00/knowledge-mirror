import io
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_public_shortlink_html_renders():
    u = User.objects.create_user("alice", password="x")
    c = APIClient()
    assert c.login(username="alice", password="x")
    f = io.BytesIO(b"hello iam hub"); f.name = "hello.txt"
    up = c.post("/api/v1/stamps/upload/", {"title": "Share Me", "file": f})
    assert up.status_code == 201
    share = c.post(f"/api/v1/stamps/{up.data['id']}/share/")
    assert share.status_code == 200
    short_url = share.data["short_url"]
    path = short_url.split("://",1)[-1].split("/",1)[-1]
    resp = c.get("/" + path, HTTP_ACCEPT="text/html")
    assert resp.status_code == 200
    assert b"Document Receipt" in resp.content