from django.contrib import admin

# Register your models here.
from chat.models import ChatSession,ChatMessage

@admin.register(ChatSession)
class ChatSessionModelAdmin(admin.ModelAdmin):
    list_display = ('id','session_uuid','first_user','second_user','started_at','ended_at')

@admin.register(ChatMessage)
class ChatMessageModelAdmin(admin.ModelAdmin):
    list_display = ('id','from_user','message','sent_at','seen')