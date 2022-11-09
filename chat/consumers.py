import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Messages, Group


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        room_name = text_data_json['room_name']
        await self.save_messages(room_name, username, message)
        await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'message': message,
                                                                   'username': username})

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({'message': message, 'username': username}))

    @sync_to_async
    def save_messages(self, room_name, username, message):
        group = Group.objects.filter(group_name=room_name).first()
        Messages.objects.create(group=group, username=username, message=message)
        