import asyncio
from websocket_client import WebSocketClient
from handlers import handle_message

TOKEN = "913b8eb2-10ce-43b4-a8c1-ffb7dd4a5376"
ROOM_KEY = "3i5i6gpvg5e96dxcn5x8it9v"

async def main():
    url = f"wss://botrisbattle.com/ws?token={TOKEN}&roomKey={ROOM_KEY}"
    client = WebSocketClient(url, handle_message)
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main())
