# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message
from group.models import Group
from account.models import User
import datetime
from django.conf import settings


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_id,
            self.channel_name
        )

        if self.scope["user"].is_anonymous:
            self.close()
        else:
            self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        pic_url = user.pic
        now_time = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)

        group = Group.objects.get(id=self.group_id)
        Message.objects.create( message=message, group=group, user=self.scope["user"])

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_id,
            {
                'type': 'chat_message',
                'message': message,
                'user': str(user),
                'pic_url':pic_url,
                'now_time': now_time
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        now_time = event['now_time']
        user = event['user']
        pic_url = event['pic_url']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'now_time': now_time,
            'pic_url':pic_url,
        }))