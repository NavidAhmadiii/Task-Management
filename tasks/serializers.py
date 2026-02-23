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
        request = self.context.get('request')
        if value and request and request.user.is_authenticated:
            if not (value.owner == request.user or request.user in value.member.all()):
                raise serializers.ValidationError(
                    'you not to allow access to this project')
        return value
