from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'start_date', 'end_date', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError({
                    "end_date": "End date must not be earlier than start date."
                })
        
        if self.instance:
            start_date = data.get('start_date', self.instance.start_date)
            end_date = data.get('end_date', self.instance.end_date)
            if start_date and end_date and end_date < start_date:
                raise serializers.ValidationError({
                    "end_date": "End date must not be earlier than start date."
                })
        
        return data
    
    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title is required.")
        return value