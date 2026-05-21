from django.test import TestCase

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Project
from datetime import date


class ProjectTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.project1 = Project.objects.create(
            title='Project 1',
            description='Description 1',
            created_by=self.user1
        )
    
    def test_create_project_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'New Project',
            'description': 'New Description',
            'status': 'planned',
            'priority': 'high'
        }
        response = self.client.post('/api/projects/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_project_unauthenticated(self):
        data = {
            'title': 'New Project',
            'description': 'New Description'
        }
        response = self.client.post('/api/projects/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_own_projects_only(self):
        self.client.force_authenticate(user=self.user1)
        Project.objects.create(title='User2 Project', description='Test', created_by=self.user2)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_cannot_access_other_user_project(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f'/api/projects/{self.project1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_project_date_validation(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Test Project',
            'description': 'Test',
            'start_date': '2024-12-01',
            'end_date': '2024-11-01'
        }
        response = self.client.post('/api/projects/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_own_project(self):
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/projects/{self.project1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.title, 'Updated Title')
    
    def test_delete_own_project(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/projects/{self.project1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(id=self.project1.id).exists())