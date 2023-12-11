from rest_framework import serializers

from thread import models
from authentication.api.v1.serializers import AddCustomUserSerializer
class CreateThreadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Thread
        fields = ['pk', 'name']
        read_only_fields = ['pk',]

    def create(self, validated_data):
        return models.Thread.objects.create(**validated_data)
    



class AddMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thread
        fields = ['members']


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = models.Messages
        fields = ['user', 'content', 'send_at']
        read_only_fields = ['user', 'send_at']

    

class ViewThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    members = AddCustomUserSerializer(many=True)
    class Meta:
        model = models.Thread
        fields = ['pk', 'name', 'members', 'messages']
    