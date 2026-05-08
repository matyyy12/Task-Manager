from rest_framework import serializers
from groups.models import Group
from user.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'members')
        read_only_fields = ['id']


class GroupMemberSerializer(serializers.ModelSerializer):
    members_details = UserSerializer(source='members', many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'members_details')
        read_only_fields = ['id']