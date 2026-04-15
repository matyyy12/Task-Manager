from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from task.models import Task
from task.serializers import TaskSerializer
from .models import Category
from .serializers import CategorySerializer


# Create your views here.


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    def get(self, request, pk):
        category = self._get_category(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request, pk):
        category = self._get_category(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = Category.objects.filter(pk=pk).first()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_category(self, pk):
        return Category.objects.filter(pk=pk).first()


class CategoryTaskView(APIView):
    def get(self, request, pk):
        category = Category.objects.filter(pk=pk).first()
        tasks = Task.objects.filter(category=category)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)