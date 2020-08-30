from django.contrib import admin

from .models import Thread, ChatMessage


class ChatMessageAdmin(admin.TabularInline):
    model = ChatMessage


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessageAdmin]

    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)
admin.site.register(ChatMessage)
