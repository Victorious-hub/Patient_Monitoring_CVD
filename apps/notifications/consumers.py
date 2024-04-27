import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notification'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, text_data):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data = text_data.strip()
        text_data_json = json.loads(str(text_data))
        print(text_data_json)
        message = text_data_json['message']
        event = {
            'type': 'send_notification',
            'message': message
        }
        await self.channel_layer.group_send(self.group_name, event)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({'message': event['message']}))
