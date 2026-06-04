from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import TaskSerializer
from tokens.authentication import BearerAuthentication
from task.models import Task


# Create your views here.


class TaskListView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filters = {}
        group_pk = request.query_params.get('group', None)
        completed = request.query_params.get('completed', None)
        filters['assigned_to'] = request.user

        if group_pk is not None:
            filters['group'] = group_pk

        if completed is not None:
            filters['completed'] = completed.lower() == 'true'

        tasks = Task.objects.filter(**filters).all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


    def post(self, request):
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                group = request.data['group']
                if not user.member.filter(pk=group).exists():
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def patch(self, request, pk):
        task = self._get_task(pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self._get_task(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_task(self, pk):
        return Task.objects.filter(pk=pk).first()
