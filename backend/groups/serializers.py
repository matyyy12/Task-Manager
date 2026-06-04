import datetime

from rest_framework import serializers
from groups.models import Group, Invitation
from user.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'description')
        read_only_fields = ['id']


class GroupMemberSerializer(serializers.ModelSerializer):
    members_details = UserSerializer(source='members', many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'members_details')
        read_only_fields = ['id']


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ("id", "token", "group", "created_by", "expired_at")
        read_only_fields = ['id', 'token']
