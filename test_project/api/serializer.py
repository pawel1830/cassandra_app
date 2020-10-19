from datetime import datetime

from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.Serializer):
    magic_number = serializers.IntegerField()
    title = serializers.CharField()
    email = serializers.EmailField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField(default=datetime.now())

    def create(self, validated_data):
        message = Message(**validated_data).save()
        return message
