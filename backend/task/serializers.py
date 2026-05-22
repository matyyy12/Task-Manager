from rest_framework import serializers
from task.models import Task
from user.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_details = UserSerializer(source = "assigned_to", read_only=True)

    def update(self, instance, validated_data):
        if validated_data.get('completed', False) is True:
            validated_data['category'] = Task.Category.DONE
        elif validated_data.get('category', "TODO") == "DONE":
            validated_data['completed'] = True
        else:
            validated_data['completed'] = False
        return super().update(instance, validated_data)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_to', 'completed', 'assigned_to', 'assigned_to_details',
                  'category', 'group']
        read_only_fields = ['id', 'assigned_to_details']