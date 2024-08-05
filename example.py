import asyncio

import botris

TOKEN = "913b8eb2-10ce-43b4-a8c1-ffb7dd4a5376"
ROOM_KEY = "wxzasc1mhqci3zdmnf3fd6ea"

async def main():
    await botris.connect(TOKEN, ROOM_KEY, botris.bots.RandomBot(), tracking=True)
    # itf = botris.Interface.create(TOKEN, ROOM_KEY, botris.bots.BlockFish(node_limit=800), tracking=False)
    # await itf.connect()

if __name__ == "__main__":
    asyncio.run(main())