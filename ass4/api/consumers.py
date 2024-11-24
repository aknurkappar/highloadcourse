import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class AudioProgressConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.upload_id = self.scope['url_route']['kwargs']['upload_id']
        self.group_name = f"audio_progress_{self.upload_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def audio_progress_update(self, event):
        await self.send(text_data=json.dumps(event))
