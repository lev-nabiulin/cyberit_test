from rest_framework import serializers
from .models import CustomUser, Task, Work


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "date_registered"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "date_created", "user"]


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ["title", "is_done", "date_done", "task"]
