from rest_framework import serializers
from .models import CustomUser, UserProfile
from phonenumber_field.serializerfields import PhoneNumberField


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["bio", "address", "city", "photo", "birth_date"]
        extra_kwargs = {"bio": {"required": False}}


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    phone_number = PhoneNumberField()
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = [
            "phone_number",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "profile",
        ]

    def validate(self, data):
        if data["password"] != data.pop("confirm_password"):
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", {})

        user = CustomUser.objects.create_user(
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        UserProfile.objects.filter(user=user).update(**profile_data)

        return user
