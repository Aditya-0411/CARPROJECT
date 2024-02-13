
# messaging/views.py
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def message_list(request):
    if request.method == 'GET':
        messages = Message.objects.filter(receiver=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        receiver_username = request.data.get('receiver')
        receiver_user = User.objects.get(username=receiver_username)

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, receiver=receiver_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def message_detail(request, receiver):
    sender = request.user
    receiver_user = User.objects.get(username=receiver)

    try:
        message = Message.objects.get(sender=sender, receiver=receiver_user)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_messages(request):
    messages = Message.objects.filter(sender=request.user)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)

        # Check if the authenticated user is the sender or receiver of the message
        if message.sender == request.user or message.receiver == request.user:
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
