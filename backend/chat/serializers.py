from rest_framework import serializers
from chat.models import ChatMessage,ChatSession
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email')

class ChatMessageSerializer(serializers.ModelSerializer):

    msg_type=serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ('message','from_user','sent_at','msg_type')

    def get_msg_type(self,obj):
        user=self.context.get('user')
        if obj.from_user==user:
            return 'sent'
        else:
            return 'received'