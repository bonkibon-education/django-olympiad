from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Role

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        fields = ("name",)
        model = Role

    def validate_name(self, value):
        return value

    def to_representation(self, instance):
        return instance.name


class CustomUserSerializer(serializers.ModelSerializer):
    """CustomUser serializer without role, for basic functions."""
    firstName = serializers.CharField(source='first_name', required=False)
    surname = serializers.CharField(source='last_name', required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('id', 'firstName', 'surname', 'username', "password")
        model = User

    def create(self, validated_data):
        """Creates and returns a user with a hashed password."""
        with transaction.atomic():
            password = validated_data['password']
            user = super().create(validated_data)
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        """Updates and returns a user with a hashed password."""
        with transaction.atomic():
            password = validated_data['password']
            instance = super().update(instance, validated_data)
            instance.set_password(password)
            instance.save()
        return instance


class CustomUserSerializerWithRole(CustomUserSerializer):
    """CustomUser serializer with role support, for admin functions."""
    role = RoleSerializer()

    class Meta:
        fields = ('id', 'firstName', 'surname', 'username', "role", "password")
        model = User

    def validate_role(self, value):
        """Ensure that a role is specified."""
        if not value:
            raise ValidationError("A role is required!")
        return value

    def create(self, validated_data):
        """Creates a user and assigns a single role."""
        role_data = validated_data.pop("role", None)
        role_name = role_data["name"] if role_data else None

        with transaction.atomic():
            new_user = super().create(validated_data)
            if role_name:
                new_role, created = Role.objects.get_or_create(name=role_name)
                new_user.role = new_role
                new_user.save()
        return new_user

    def update(self, instance, validated_data):
        """Updates a user and assigns a new role if provided."""
        role_data = validated_data.pop("role", None)
        role_name = role_data["name"] if role_data else None

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if role_name:
                new_role, created = Role.objects.get_or_create(name=role_name)
                instance.role = new_role
                instance.save()
        return instance


class SignOutSerializer(serializers.Serializer):
    """Serializer to confirm sign-out."""

    def to_representation(self, instance):
        return {"details": "signed out successfully"}

    def to_internal_value(self, data):
        return {"details": "signed out successfully"}


class CustomTokenVerifySerializer(serializers.Serializer):
    """Serializer for verifying token validity."""

    valid = serializers.BooleanField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer for obtaining JWT access and refresh tokens."""

    def validate(self, attrs):
        """Return access and refresh tokens."""
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data
