from rest_framework import serializers
from django.utils import timezone
from .models import Task
from projects.models import Project


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'project', 'project_title', 'title', 'description',
            'status', 'priority', 'due_date', 'is_completed',
            'assigned_to', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'is_completed', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title is required.")
        return value
    
    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date must not be earlier than the current date.")
        return value
    
    def validate_project(self, value):
        user = self.context['request'].user
        if value.created_by != user:
            raise serializers.ValidationError("You can only create tasks under your own projects.")
        return value
    
    def validate(self, data):
        if self.instance:
            project = data.get('project', self.instance.project)
        else:
            project = data.get('project')
        
        if project:
            user = self.context['request'].user
            if project.created_by != user:
                raise serializers.ValidationError({
                    "project": "You can only create tasks under your own projects."
                })
        
        return data