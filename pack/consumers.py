from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AppItemsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Example: Send initial data on connection
        data = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]
        await self.send(json.dumps(data))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Handle incoming messages (if needed)
        message = json.loads(text_data)
        print("Received message:", message)
