from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Task, Work
from .serializers import TaskSerializer, WorkSerializer
import json


class BaseViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.task = Task.objects.create(title="Test Task", user=cls.user)
        cls.work = Work.objects.create(title="Test Work", is_done=False, task=cls.task)


class TaskAPITestCase(BaseViewTest):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_task_list(self):
        response = self.client.get(reverse("task-list"))
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_get_task_detail(self):
        response = self.client.get(reverse("task-detail", kwargs={"pk": self.task.id}))
        task = Task.objects.get(id=self.task.id)
        serializer = TaskSerializer(task)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        new_title = "Updated Task Title"
        response = self.client.put(
            reverse("task-detail", kwargs={"pk": self.task.id}),
            json.dumps(
                {
                    "title": new_title,
                    "user": self.user.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, new_title)

    def test_delete_task(self):
        response = self.client.delete(
            reverse("task-detail", kwargs={"pk": self.task.id})
        )
        self.assertEqual(response.status_code, 204)


class WorkAPITestCase(BaseViewTest):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_work_list(self):
        response = self.client.get(reverse("work-list"))
        works = Work.objects.all()
        serializer = WorkSerializer(works, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_get_work_detail(self):
        response = self.client.get(reverse("work-detail", kwargs={"pk": self.work.id}))
        work = Work.objects.get(id=self.work.id)
        serializer = WorkSerializer(work)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_update_work(self):
        new_title = "Updated Work Title"
        response = self.client.put(
            reverse("work-detail", kwargs={"pk": self.work.id}),
            json.dumps(
                {"title": new_title, "is_done": self.work.is_done, "task": self.task.id}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.work.refresh_from_db()
        self.assertEqual(self.work.title, new_title)

    def test_delete_work(self):
        response = self.client.delete(
            reverse("work-detail", kwargs={"pk": self.work.id})
        )
        self.assertEqual(response.status_code, 204)
