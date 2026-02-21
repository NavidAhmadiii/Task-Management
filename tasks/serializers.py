from rest_framework import serializers
from django.utils import timezone
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

        def validate_due_date(self, value):
            '''Ensure the due date is in the future.'''
            if value and value < timezone.now():
                raise serializers.ValidationError(
                    "Due date must be in the future.")
            return value
