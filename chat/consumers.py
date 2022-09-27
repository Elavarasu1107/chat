import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Messages


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
        Messages.objects.create(room_name=room_name, username=username, message=message)

# import json
# from asgiref.sync import sync_to_async, async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# from .models import Chat, User, Messages


# class ChatConsumer(WebsocketConsumer):

#     def fetch_messages(self, data):
#         messages = Messages.objects.all()
#         content = {'messages': self.messages_to_json(messages)}
#         self.send_message(content)

#     def new_message(self, data):
#         user = User.objects.filter(username=data.get('author'))[0]
#         message = Messages.objects.create(username=user, message=data.get('message'))
#         content = {'command': 'new_message', 'message': self.message_to_json(message)}
#         return self.send_chat_message(content)


#     def messages_to_json(self, messages):
#         result = []
#         for message in messages:
#             result.append(self.message_to_json(message))
#         return result

#     def message_to_json(self, message):
#         return {'author': message.username, 'message': message.message, 'time': str(message.created_at)}

#     commands = {'fetch_messages': fetch_messages, 'new_message': new_message}

#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         self.commands.get(data.get('command'))(self, data)

#     def send_chat_message(self, message):
#         # message = data['message']
#         # username = data['username']
#         # room_name = data['room_name']
#         # self.save_messages(room_name, username, message)
#         async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'chat_message', 'message': message})

#     def send_message(self, message):
#         self.send(text_data=json.dumps(message))

#     def chat_message(self, event):
#         message = event['message']
#         # username = event['username']
#         self.send(text_data=json.dumps(message))

    # @sync_to_async
    # def save_messages(self, room_name, username, message):
    #     Messages.objects.create(room_name=room_name, username=username, message=message)
