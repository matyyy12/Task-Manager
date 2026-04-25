from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from task.models import Task
from tokens.models import Token
from tokens.authentication import BearerAuthentication
from task.serializers import TaskSerializer
from user.serializers import UserSerializer
from django.contrib.auth.hashers import check_password


# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class UserListView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token(user=user)
            token.access_token = Token.generate_key()
            token.refresh_token = Token.generate_key()
            token.access_expires_at = Token.get_access_expiry()
            token.refresh_expires_at = Token.get_refresh_expiry()
            token.save()
            return Response({'access_token': token.access_token,
                              'refresh_token': token.refresh_token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    authentication_classes = [BearerAuthentication]

    def get(self, request):
        user = request.user
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if check_password(request.data.get("password"), user.password):
            user.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class UserTaskView(APIView):
    authentication_classes = [BearerAuthentication]

    def get(self, request):
        user = request.user
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
