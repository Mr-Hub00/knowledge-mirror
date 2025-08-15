import io
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_upload_stamps_creates_record():
    user = User.objects.create_user("test", password="x")
    client = APIClient()
    client.login(username="test", password="x")

    f = io.BytesIO(b"hello iam hub")
    f.name = "hello.txt"

    resp = client.post("/api/v1/stamps/upload/", {"title": "Doc", "file": f}, format="multipart")
    assert resp.status_code == 201
    data = resp.json()
    assert "sha256" in data and data["title"] == "Doc"

    list_resp = client.get("/api/v1/stamps/")
    assert list_resp.status_code == 200
    results = list_resp.json()
    if isinstance(results, dict) and "results" in results:
        results = results["results"]
    assert any(row["id"] == data["id"] for row in results)