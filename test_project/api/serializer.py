from django.utils.timezone import now

from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.Serializer):
    magic_number = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    content = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(default=now, read_only=True)

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message
