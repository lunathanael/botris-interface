import asyncio

from bots.blockfish import BlockFish
from interface import Interface

TOKEN = "913b8eb2-10ce-43b4-a8c1-ffb7dd4a5376"
ROOM_KEY = "1aqny49hn5rcvh3qx140cpx1"

async def main():
    itf = Interface.create(TOKEN, ROOM_KEY, BlockFish(node_limit=8000), tracking=False)
    await itf.connect()

if __name__ == "__main__":
    asyncio.run(main())
