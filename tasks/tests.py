from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from projects.models import Project
from .models import Task
from datetime import date, timedelta


class TaskTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.project1 = Project.objects.create(
            title='Project 1',
            description='Description',
            created_by=self.user1
        )
        self.project2 = Project.objects.create(
            title='Project 2',
            description='Description',
            created_by=self.user2
        )
        self.task1 = Task.objects.create(
            project=self.project1,
            title='Task 1',
            description='Description',
            due_date=date.today() + timedelta(days=7),
            created_by=self.user1
        )
    
    def test_create_task_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'project': self.project1.id,
            'title': 'New Task',
            'description': 'Description',
            'due_date': date.today() + timedelta(days=7),
            'status': 'todo',
            'priority': 'high'
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_task_unauthenticated(self):
        data = {
            'project': self.project1.id,
            'title': 'New Task',
            'description': 'Description',
            'due_date': date.today() + timedelta(days=7)
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_cannot_create_task_under_other_user_project(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'project': self.project2.id,
            'title': 'New Task',
            'description': 'Description',
            'due_date': date.today() + timedelta(days=7)
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_own_tasks_only(self):
        self.client.force_authenticate(user=self.user1)
        Task.objects.create(
            project=self.project2,
            title='User2 Task',
            description='Test',
            due_date=date.today() + timedelta(days=7),
            created_by=self.user2
        )
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_cannot_access_other_user_task(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_task_completion_flag_when_status_done(self):
        self.client.force_authenticate(user=self.user1)
        data = {'status': 'done'}
        response = self.client.patch(f'/api/tasks/{self.task1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_completed)
    
    def test_task_completion_flag_when_status_not_done(self):
        self.task1.status = 'done'
        self.task1.save()
        self.client.force_authenticate(user=self.user1)
        data = {'status': 'in_progress'}
        response = self.client.patch(f'/api/tasks/{self.task1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertFalse(self.task1.is_completed)
    
    def test_task_due_date_validation(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'project': self.project1.id,
            'title': 'Test Task',
            'description': 'Test',
            'due_date': date.today() - timedelta(days=1)
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_filter_tasks_by_status(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/tasks/?status=todo')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_tasks(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/tasks/?search=Task')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_order_tasks(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/tasks/?ordering=-created_at')
        self.assertEqual(response.status_code, status.HTTP_200_OK)