import asyncio

from bots import BlockFish
from interface import Interface

TOKEN = "913b8eb2-10ce-43b4-a8c1-ffb7dd4a5376"
ROOM_KEY = "u0m8op7maqb22nqg8r4mfjiy"

async def main():
    itf = Interface.create(TOKEN, ROOM_KEY, BlockFish(node_limit=8000), tracking=False)
    await itf.connect()

if __name__ == "__main__":
    asyncio.run(main())
