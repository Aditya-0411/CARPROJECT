# # messaging/serializers.py
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Message
#
# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Message
#         fields = ['id', 'sender', 'receiver', 'content', 'timestamp']

# messaging/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    # Add serializers for sender and receiver to handle username strings

    sender = serializers.CharField(source='sender.username', read_only=True)
    receiver = serializers.CharField(source='receiver.username')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']
