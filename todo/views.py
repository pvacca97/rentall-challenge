from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from todo.models import Task, Category
from todo.serializers import TaskSerializer, CategorySerializer


class TaskList(APIView):
    def get(self, request):
        task_list = Task.objects.all().order_by('id')
        serializer = TaskSerializer(task_list, many=True)
        task_list_dict = {'task_list': serializer.data}
        return Response(task_list_dict, status=status.HTTP_200_OK)


class TaskDetail(APIView):
    def get_task(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task = self.get_task(pk=pk)
        serializer = TaskSerializer(task)
        task_dict = {'task': serializer.data}
        return Response(task_dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            task_dict = {'task': serializer.data}
            return Response(task_dict, status=status.HTTP_201_CREATED)
        error_dict = {'error': serializer.errors}
        return Response(error_dict, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_task(pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        task = self.get_task(pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            task_dict = {'task': serializer.data}
            return Response(task_dict, status=status.HTTP_200_OK)
        error_dict = {'error': serializer.errors}
        return Response(error_dict, status=status.HTTP_400_BAD_REQUEST)


class CategoryList(APIView):
    def get(self, request):
        category_list = Category.objects.all().order_by('name')
        serializer = CategorySerializer(category_list, many=True)
        category_list_dict = {'category_list': serializer.data}
        return Response(category_list_dict, status=status.HTTP_200_OK)


class CategoryDetail(APIView):
    def get_category(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_category(pk=pk)
        serializer = CategorySerializer(category)
        category_dict = {'category': serializer.data}
        return Response(category_dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            category_dict = {'category': serializer.data}
            return Response(category_dict, status=status.HTTP_201_CREATED)
        error_dict = {'error': serializer.errors}
        return Response(error_dict, status=status.HTTP_400_BAD_REQUEST)
