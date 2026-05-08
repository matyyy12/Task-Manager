from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from groups.models import Group
from groups.serializers import GroupSerializer, GroupMemberSerializer
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
            serializer.save()
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
