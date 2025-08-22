from rest_framework import serializers
from core.models import MemberProfile, DocumentStamp, Contribution

class MemberProfileSer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = ["id", "user", "proof_of_humanity_id", "ancestry_card", "created_at"]

class DocumentStampSer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = DocumentStamp
        fields = ["id", "owner", "title", "ipfs_cid", "sha256", "timestamped_at"]
        read_only_fields = ["owner", "ipfs_cid", "sha256", "timestamped_at"]

class ContributionSer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ["id", "member", "kind", "amount", "note", "created_at"]