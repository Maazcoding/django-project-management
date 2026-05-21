from django_filters import rest_framework as filters
from .models import Project


class ProjectFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='start_date')
    end_date = filters.DateFilter(field_name='end_date')
    
    class Meta:
        model = Project
        fields = {
            'status': ['exact'],
            'priority': ['exact'],
            'start_date': ['exact'],
            'end_date': ['exact'],
        }