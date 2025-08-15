import pytest
from django.contrib.auth.models import User
from core.models import DocumentStamp

@pytest.mark.django_db
def test_stamp_create():
    u = User.objects.create_user("alice", password="x")
    s = DocumentStamp.objects.create(owner=u, title="Doc", ipfs_cid="mock", sha256="abc")
    assert s.owner.username == "alice"