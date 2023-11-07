from channels.consumer import AsyncConsumer
from .models import Report, Order
import asyncio
import json

connections = {}


class SiteTable(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, text_data: dict):
        data = json.loads(text_data['text'])
        connections[data['message']] = self

    async def websocket_disconnect(self, event):
        key = list(connections.keys())[list(connections.values()).index(self)]
        del connections[key]


async def send_browser_report(order_uuid, report: Report):
    if order_uuid in connections:
        await connections[order_uuid].send({
            "type": "websocket.send",
            "text": json.dumps({
                'number': report.phone_number,
                'device': report.user_agent,
                'email': report.mail,
                'text': report.report_text
            })
        })
