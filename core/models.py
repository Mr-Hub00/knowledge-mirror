from django.db import models
from django.contrib.auth.models import User

class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    proof_of_humanity_id = models.CharField(max_length=128, blank=True)
    ancestry_card = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentStamp(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    ipfs_cid = models.CharField(max_length=128, blank=True)
    sha256 = models.CharField(max_length=64, blank=True)
    timestamped_at = models.DateTimeField(auto_now_add=True)
    share_token = models.CharField(max_length=64, unique=True, null=True, blank=True)
    share_token_expires_at = models.DateTimeField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verify_txid = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        ordering = ["-timestamped_at"]

class Contribution(models.Model):
    KIND_CHOICES = [("education","education"),("governance","governance"),("service","service")]
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.CharField(max_length=32, choices=KIND_CHOICES)
    amount = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verify_txid = models.CharField(max_length=128, blank=True, default="")
    share_token = models.CharField(max_length=64, unique=True, null=True, blank=True)
    share_token_expires_at = models.DateTimeField(null=True, blank=True)