from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

# Create your views here.


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        '''every user can only see their own tasks.'''
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        '''Set the user field to the current user when creating a task.'''
        serializer.save(user=self.request.user)
