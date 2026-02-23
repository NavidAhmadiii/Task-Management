from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Project
from .serializers import PorjectSerializer
from .permission import IsOwnerOrReadOnly

# Create your views here.

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = PorjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        '''Return projects where the user is a member.'''
        user = self.request.user
        return Project.objects.filter(members=user).distinct()

    def perform_create(self, serializer):
        '''Set the owner as the user creating the project.'''
        Project = serializer.save(owner=self.request.user)
        Project.members.add(self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_member(self, request, pk=None):
        '''Add a member to the project. Only the owner can add members.'''
        project = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user in project.members.all():
            return Response({'error': 'User is already a member'}, status=status.HTTP_400_BAD_REQUEST)

        project.members.add(user)
        return Response({'message': 'Member added successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_member(self, request, pk=None):
        '''Remove a member from the project. Only the owner can remove members.'''
        project = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user not in project.members.all():
            return Response({'error': 'User is not a member'}, status=status.HTTP_400_BAD_REQUEST)

        project.members.remove(user)
        return Response({'message': 'Member removed successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        '''Get all tasks for the project.'''
        project = self.get_object()
        tasks = project.tasks.all()
        from tasks.serializers import TaskSerializer
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
