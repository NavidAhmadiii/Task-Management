from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        '''every user can only see their own tasks.'''
        user = self.request.user
        return Task.objects.filter(Q(user=user) | Q(project__members=user)).distinct()

    def perform_create(self, serializer):
        '''Set the user field to the current user when creating a task.'''
        serializer.save(user=self.request.user)

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['-created_at']
