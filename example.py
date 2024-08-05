import asyncio

import botris

TOKEN = "913b8eb2-10ce-43b4-a8c1-ffb7dd4a5376"
ROOM_KEY = "wxzasc1mhqci3zdmnf3fd6ea"

import asyncio


async def main():
    itf: botris.Interface = await botris.connect(
        TOKEN,
        ROOM_KEY,
        botris.bots.RandomBot(),
        tracking=False,
        threading=True,
        daemon=True,
    )
    itf2: botris.Interface = await botris.connect(
        TOKEN,
        ROOM_KEY,
        botris.bots.RandomBot(),
        tracking=False,
        threading=True,
        daemon=True,
    )
    await asyncio.sleep(100)
    # itf = botris.Interface.create(TOKEN, ROOM_KEY, botris.bots.BlockFish(node_limit=800), tracking=False)
    # await itf.connect()


if __name__ == "__main__":
    asyncio.run(main())
