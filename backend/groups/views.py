import datetime
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from groups.models import Group, Invitation
from groups.serializers import GroupSerializer, GroupMemberSerializer, InvitationSerializer
from tokens.authentication import BearerAuthentication

# Create your views here.


class GroupListView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        groups = Group.objects.filter(members__in=[user]).all()
        serializer = GroupSerializer(groups, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            group.members.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        group = Group.objects.filter(pk=pk).first()
        if group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GroupMemberSerializer(group)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request, pk):
        group = Group.objects.filter(pk=pk).first()
        if group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        group.members.add(request.user)
        return Response(status=status.HTTP_200_OK)


    def delete(self, request, pk):
        group = Group.objects.filter(pk=pk).first()
        if group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        group.members.remove(request.user)
        return Response(status=status.HTTP_200_OK)


class InvitationView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        group = Group.objects.filter(pk=pk).first()
        if group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        invitation = Invitation.objects.create(created_by=user, group=group,
                                               expired_at=timezone.now() + datetime.timedelta(days=1))
        serializer = InvitationSerializer(invitation)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


    def get(self, request, token):
        user = request.user
        invitation = Invitation.objects.filter(token=token).first()
        if invitation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if invitation.expired_at < timezone.now():
            return Response(status=status.HTTP_404_NOT_FOUND)
        if invitation.group.members.filter(pk=user.pk).exists():
            return Response({"detail": "You are already in this group."}, status=status.HTTP_400_BAD_REQUEST)

        invitation.group.members.add(user)
        serializer = GroupSerializer(invitation.group)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

