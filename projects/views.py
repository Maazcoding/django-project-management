from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsOwner
from .filters import ProjectFilter


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ProjectFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'priority']
    
    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)