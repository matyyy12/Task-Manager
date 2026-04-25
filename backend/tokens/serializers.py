from rest_framework import serializers
from tokens.models import Token

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('user', 'access_token', 'refresh_token', 'access_expires_at', 'refresh_expires_at', 'created_at')
        read_only_fields = ('user', 'access_token', 'refresh_token', 'access_expires_at', 'refresh_expires_at', 'created_at')