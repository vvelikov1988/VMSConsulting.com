from rest_framework import serializers

from .models import Thread, ChatMessage
from account.serializers import AccountSerializer


class ChatMessagesSerializer(serializers.ModelSerializer):
    thread = serializers.RelatedField(source='chatmessage', read_only=True)
    user = AccountSerializer()

    class Meta:
        model = ChatMessage
        fields = ['thread', 'user', 'message', 'timestamp']


class MessageSerializer(serializers.ModelSerializer):
    chatmessage = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ['first', 'second', 'chatmessage']
