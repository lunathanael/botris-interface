import asyncio

from interface.handlers import handle_message
from interface.websocket_client import WebSocketClient

TOKEN = "913b8eb2-10ce-43b4-a8c1-ffb7dd4a5376"
ROOM_KEY = "sbkkfis8h0kh6dnkibeawb2q"

async def main():
    url = f"wss://botrisbattle.com/ws?token={TOKEN}&roomKey={ROOM_KEY}"
    client = WebSocketClient(url, handle_message)
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main())
