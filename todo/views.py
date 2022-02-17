from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from todo.models import Task
from todo.serializers import TaskSerializer


class TaskList(APIView):
    def get(self, request):
        task_list = Task.objects.all()
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
