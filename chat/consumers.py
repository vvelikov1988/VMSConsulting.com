import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        sender = self.scope['user']
        receiver = self.scope['url_route']['kwargs']['username']
        thread_obj = await self.get_thread(sender, receiver)

        chat_room = 'thread_%s' % thread_obj.id

        self.thread_obj = thread_obj
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self, event):
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)

            msg = loaded_dict_data.get('message')
            user = self.scope['user']
            if user.is_authenticated:
                username = user.username

            response = {
                'message': msg,
                'username': username,
                'user_pic': user.profile_pic.thumbnail.url,
            }
            await self.create_chat_message(user, msg)

            # broadcasts the message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
                }
            )

    async def chat_message(self, event):
        # send the actual message
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        pass

    @database_sync_to_async
    def get_thread(self, sender, receiver):
        return Thread.objects.get_or_new(sender, receiver)[0]

    @database_sync_to_async
    def create_chat_message(self, sender, message):
        return ChatMessage.objects.create(thread=self.thread_obj, user=sender, message=message)
