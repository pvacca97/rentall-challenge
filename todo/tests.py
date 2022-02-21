from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from todo.models import Task, Category
from todo.serializers import TaskSerializer, CategorySerializer


class TaskDetailTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testadmin'
        )
        self.client.force_authenticate(self.user)
        self.category = Category.objects.create(name='category_1')

    def test_get_task_detail(self):
        Task.objects.create(
            id='1', title='test_title',
            description='test_description',
            date='2020-01-01', is_checked='False',
            category=self.category
        )
        response = self.client.get('/task/1/')
        task = Task.objects.get(pk=1)
        serializer = TaskSerializer(task)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task'], serializer.data)

    def test_post_task_detail(self):
        payload = {
            'title': 'test_title',
            'description': 'test_description',
            'date': '2020-01-01',
            'isChecked': 'false'
        }
        response = self.client.post('/task/', payload)
        task_exists = Task.objects.filter(id=response.data['task']['id']).exists()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(task_exists)

    def test_delete_task_detail(self):
        Task.objects.create(
            id='1', title='test_title',
            description='test_description',
            date='2020-01-01', is_checked='False'
        )
        response = self.client.delete('/task/1/')
        task_exists = Task.objects.filter(id=1).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(task_exists)

    def test_patch_title_task_detail(self):
        post_payload = {
            'title': 'test_title',
            'description': 'test_description',
            'date': '2020-01-01',
            'isChecked': 'false'
        }
        patch_payload = {
            'title': 'updated_test_title',
        }
        response = self.client.post('/task/', post_payload)
        task = response.data['task']
        task_id = task['id']
        response = self.client.patch(f'/task/{task_id}/', patch_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task']['title'], patch_payload['title'])
        self.assertEqual(response.data['task']['description'], post_payload['description'])
        self.assertEqual(response.data['task']['date'], post_payload['date'])
        self.assertEqual(response.data['task']['is_checked'], False)

    def test_patch_all_task_detail(self):
        post_payload = {
            'title': 'test_title',
            'description': 'test_description',
            'date': '2020-01-01',
            'isChecked': 'false'
        }
        patch_payload = {
            'title': 'updated_test_title',
            'description': 'updated_test_description',
            'date': '2020-11-11',
            'isChecked': 'true'
        }
        response = self.client.post('/task/', post_payload)
        task = response.data['task']
        task_id = task['id']
        response = self.client.patch(f'/task/{task_id}/', patch_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task']['title'], patch_payload['title'])
        self.assertEqual(response.data['task']['description'], patch_payload['description'])
        self.assertEqual(response.data['task']['date'], patch_payload['date'])
        self.assertEqual(response.data['task']['is_checked'], True)

    def test_get_task_list(self):
        Task.objects.create(
            id='1', title='test_title1',
            description='test_description1',
            date='2020-01-01', is_checked='False',
            category=self.category
        )
        Task.objects.create(
            id='2', title='test_title2',
            description='test_description2',
            date='2020-01-01', is_checked='False',
            category=self.category
        )
        response = self.client.get('/tasks/')
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task_list'], serializer.data)

    def test_error_404(self):
        response = self.client.get('/task/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertRaises(Task.DoesNotExist)

    def test_error_400(self):
        payload = {
            'title': 'test_title',
            'description': 'test_description',
            'date': '2020-01-01',
            'isChecked': '1234'
        }
        response = self.client.post('/task/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestCategoryDetail(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testadmin'
        )
        self.client.force_authenticate(self.user)

    def test_get_category_list(self):
        Category.objects.create(
            name='test_category2'
        )
        Category.objects.create(
            name='test_category3'
        )
        response = self.client.get('/categories/')
        category_list = Category.objects.all()
        serializer = CategorySerializer(category_list, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category_list'], serializer.data)

    def test_get_category_detail(self):
        Category.objects.create(
            name='test_category_2'
        )
        response = self.client.get('/category/test_category_2/')
        category = Category.objects.get(pk='test_category_2')
        serializer = CategorySerializer(category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category'], serializer.data)

    def test_post_category_detail(self):
        payload = {
            'name': 'category_2'
        }
        response = self.client.post('/category/', payload)
        category_exists = Category.objects.filter(name=response.data['category']['name']).exists()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(category_exists)
