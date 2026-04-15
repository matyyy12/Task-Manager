from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from task.models import Task
from .models import User
from task.serializers import TaskSerializer
from user.serializers import UserSerializer


# Create your views here.


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        if not users.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, pk):
        user = self._get_user(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = self._get_user(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self._get_user(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_user(self, pk):
        return User.objects.filter(pk=pk).first()


class UserTaskView(APIView):
    def get(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        completed = request.query_params.get('completed')

        if completed:
            completed = completed.lower() == 'true'
            tasks = Task.objects.filter(completed=completed)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)

        tasks = user.assigned_to.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
