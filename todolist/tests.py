from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task_char
import uuid


class TaskListViewTest(TestCase):
    def setUp(self):
        # ������� ������������
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # ������� ������
        self.client = Client()
        
        # ������� ������������
        self.client.login(username='testuser', password='testpass')

        # ������� ������
        self.task1 = Task_char.objects.create(user=self.user, title='Test Task 1', description='Test Description 1')
        self.task2 = Task_char.objects.create(user=self.user, title='Test Task 2', description='Test Description 2')

    def test_get_all_tasks(self):
        url = reverse('tasks')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        tasks = response.context['tasks']

        task_list = [
            {'title': task.title, 'description': task.description}
            for task in tasks
        ]

        print("Tasks List:")
        for task in task_list:
            print(f"Title: {task['title']}, Description: {task['description']}")

        # ��������� ������
        expected_tasks = [
            {'title': 'Test Task 1', 'description': 'Test Description 1'},
            {'title': 'Test Task 2', 'description': 'Test Description 2'}
        ]

        # ��������� ������������ ������
        self.assertEqual(task_list, expected_tasks)
        

class TaskDetailViewTest(TestCase):
    def setUp(self):
        # ������� ������������
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # ������� ������
        self.client = Client()
        
        # ������� ������������
        self.client.login(username='testuser', password='testpass')

        # ������� ������
        self.task = Task_char.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            completed=False,
            created_at = timezone.now()
        )

    def test_get_task_detail(self):
        url = reverse('task', args=[self.task.id])
        response = self.client.get(url)

        # ��������� ������-��� ������
        self.assertEqual(response.status_code, 200)

        formatted_created_at = self.task.created_at.strftime('%Y-%m-%d %H:%M:%S')

        # ���������, ��� HTML �������� ��������� ������
        self.assertContains(response, self.task.title)
        self.assertContains(response, self.task.description)
        self.assertContains(response, self.task.completed)
        self.assertContains(response, self.task.user)
        self.assertContains(response, formatted_created_at)
        

class TaskCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_create_task(self):
        url = reverse('task-create')
        
        data = {
            'title': 'New Task',
            'description': 'This is a new task description',
            'completed': False,
            'created_at': timezone.now(),  # ������������� ������� ���� � �����
        }
        
        # ���������� POST-������ �� �������� ������
        response = self.client.post(url, data)
        
        # ���������, ��� ������ ���� ������� (��������������� �� success_url)
        self.assertEqual(response.status_code, 302)
        
        # ���������, ��� ������ ��������� � ���� ������
        self.assertEqual(Task_char.objects.count(), 1)
        task = Task_char.objects.first()
        
        self.assertEqual(task.title, data['title'])
        self.assertEqual(task.description, data['description'])
        self.assertEqual(task.completed, data['completed'])
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.created_at.replace(microsecond=0), data['created_at'].replace(microsecond=0))    
        # ����� ��������� ������� � ����������� ��� � ���� �������� ��������� �����


class TaskUpdateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.task = Task_char.objects.create(
            title='Original Title',
            description='Original Description',
            user=self.user
        )
        self.update_url = reverse('task-update', kwargs={'pk': self.task.id})

    def test_update_task_success(self):
        new_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'completed': True
        }

        response = self.client.post(self.update_url, data=new_data)

        # ���������, ��� ��������������� ���������
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, new_data['title'])
        self.assertEqual(self.task.description, new_data['description'])
        self.assertTrue(self.task.completed)

    def test_update_task_not_found(self):
        invalid_id = uuid.uuid4()
        update_url = reverse('task-update', kwargs={'pk': invalid_id})
        response = self.client.post(update_url, data={})

        # ���������, ��� ������������ 404 Not Found
        self.assertEqual(response.status_code, 404)

class TaskDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        
        self.task = Task_char.objects.create(
            title='Test Task',
            description='This is a test task.',
            user=self.user
        )
        self.delete_url = reverse('task-delete', kwargs={'pk': self.task.id})

    def test_delete_task_success(self):
        # ��������, ��� ������ ���������� �� ��������
        self.assertEqual(Task_char.objects.count(), 1)

         # ��������� ������ �� �������� ������
        response = self.client.delete(self.delete_url)

        # ���������, ��� ��������� ���������������
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=f"{reverse('tasks')}?order=asc&sort=updated_at")

    def test_delete_task_not_found(self):
        # ������� ������� ������ � �������������� ID
        invalid_id = uuid.uuid4()
        response = self.client.delete(reverse('task-delete', kwargs={'pk': invalid_id}))

        # ���������, ��� ������������ 404 Not Found
        self.assertEqual(response.status_code, 404)