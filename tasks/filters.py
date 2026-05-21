from django_filters import rest_framework as filters
from .models import Task


class TaskFilter(filters.FilterSet):
    due_date = filters.DateFilter(field_name='due_date')
    
    class Meta:
        model = Task
        fields = {
            'status': ['exact'],
            'priority': ['exact'],
            'project': ['exact'],
            'is_completed': ['exact'],
            'due_date': ['exact'],
        }