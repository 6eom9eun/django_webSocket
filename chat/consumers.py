from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # group join
        # sync_to_sync 비동기
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # WebSocket connecting
        await self.accept()

    async def disconnect(self, close_code):
        # 그룹에서 Leave
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    # WebSocket의 메세지 receive
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # room group 에게 메세지 send
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    # room group 에서 메세지 receive
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        
        # WebSocket으로 메세지 전송
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))