# scraper/serializers.py
from rest_framework import serializers
from .models import Job, Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['coin', 'output', 'status']

class JobSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ['job_id', 'status', 'tasks']
