import asyncio

from interface import Interface

from bots import BlockFish

TOKEN = "913b8eb2-10ce-43b4-a8c1-ffb7dd4a5376"
ROOM_KEY = "8isznvz1ngmey257fzk7zkgb"

async def main():
    itf = Interface.create(TOKEN, ROOM_KEY, BlockFish(node_limit=1000))
    await itf.connect()

if __name__ == "__main__":
    asyncio.run(main())
