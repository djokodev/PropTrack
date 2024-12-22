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
    current_owner = serializers.SerializerMethodField()

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

    def get_current_owner(self, obj):
        return obj.current_owner.last_name if obj.current_owner else None


class PropertyTransferSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
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

    def get_from_user(self, obj):
        return str(obj.from_user.last_name) if obj.from_user.phone_number else None

    def get_to_user(self, obj):
        if obj.to_user.phone_number:
            return str(obj.to_user.phone_number)
        return None
