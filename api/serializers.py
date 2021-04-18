from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.scan import Scan
from .models.user import User
from .models.item import Item
from .models.material import Material

class ScanGetSerializer(serializers.ModelSerializer):
    """serializer for get this includes the owners email"""
    owner = serializers.StringRelatedField()
    class Meta:
        model = Scan
        fields = ('id', 'name', 'recycleable', 'description', 'material', 'owner', 'barcode', 'created_at', 'updated_at')

class ItemGetSerializer(serializers.ModelSerializer):
    """serializer for get this includes the owners email"""
    owner = serializers.StringRelatedField()
    material = serializers.StringRelatedField()
    class Meta:
        model = Item
        fields = ('id', 'name', 'recycleable', 'description', 'material', 'owner', 'barcode', 'created_at', 'updated_at')

class ScanSerializer(serializers.ModelSerializer):
    """serializer for posting """
    class Meta:
        model = Scan
        fields = ('id', 'name', 'recycleable', 'description', 'material', 'owner', 'barcode', 'created_at', 'updated_at')

class MaterialSerializer(serializers.ModelSerializer):
    """serializer for posting """
    class Meta:
        model = Material
        fields = ('id', 'name', 'recycleable')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'recycleable', 'description', 'material', 'owner', 'barcode', 'created_at', 'updated_at')

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'is_active', 'is_superuser')

class UserSerializer(serializers.ModelSerializer):
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = { 'password': { 'write_only': True, 'min_length': 5 } }

    # This create method will be used for model creation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserRegisterSerializer(serializers.Serializer):
    # Require email, password, and password_confirmation for sign up
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError('Please include a password and password confirmation.')
        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Please make sure your passwords match.')
        # if all is well, return the data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)

class ChangeUserActiveSerializer(serializers.Serializer):
    model = get_user_model()
    is_active = serializers.BooleanField(required=True)

    def update(self, instance, validated_data):
        instance.is_active = validated_data.get('is_active', instance.is_active)
        return instance
