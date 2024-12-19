from rest_framework import serializers
from .models import Property, PropertyImage, PropertyTransfer
from django.contrib.auth import get_user_model


User = get_user_model()


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "image", "created_at"]


class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    current_owner = serializers.ReadOnlyField(source="current_owner.phone_number")

    class Meta:
        model = Property
        fields = [
            "id",
            "name",
            "description",
            "value",
            "purchase_date",
            "current_owner",
            "status",
            "created_at",
            "updated_at",
            "images",
        ]
        read_only_fields = ["status", "current_owner"]


class PropertyTransferSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source="from_user.phone_number")
    to_user = serializers.SlugRelatedField(
        slug_field="phone_number",
        queryset=User.objects.all(),
    )
    property_details = PropertySerializer(source="property", read_only=True)

    class Meta:
        model = PropertyTransfer
        fields = [
            "id",
            "property",
            "property_details",
            "from_user",
            "to_user",
            "transfer_date",
            "status",
            "transfer_notes",
            "transfer_amount",
        ]
        read_only_fields = ["transfer_date", "status"]
