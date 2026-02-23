from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PorjectSerializer(serializers.ModelSerializer):
    '''Serializer for Project model.
    for list and create project.'''

    owner = UserSimpleSerializer(read_only=True)
    members = UserSimpleSerializer(many=True, read_only=True)
    take_count = serializers.IntegerField(source='tasks.count', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner',
                  'members', 'task_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']


class ProjectDetailSerializer(PorjectSerializer):
    '''Serializer for Project model.
    for retrieve and update project.
    can be use for list and create project.'''
    owner = UserSimpleSerializer(read_only=True)
    members = UserSimpleSerializer(many=True, read_only=True)
    tasks = serializers.StringRelatedField(many=True, read_only=True)

    class Meta(PorjectSerializer.Meta):
        fields = ['id', 'name', 'description', 'owner',
                  'members', 'tasks', 'created_at', 'updated_at']
