# botris-interface

[![GitHub license](https://img.shields.io/github/license/lunathanael/botris-interface)](https://github.com/lunathanael/botris-interface/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/lunathanael/botris-interface)](https://github.com/lunathanael/botris-interface/issues)
[![GitHub stars](https://img.shields.io/github/stars/lunathanael/botris-interface?style=social)](https://github.com/lunathanael/botris-interface/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/lunathanael/botris-interface?style=social)](https://github.com/lunathanael/botris-interface/network/members)
[![Wheels](https://github.com/lunathanael/botris-interface/actions/workflows/build_wheels.yml/badge.svg)](https://github.com/lunathanael/botris-interface/actions/workflows/build_wheels.yml)

botris-interface is a performant library designed for creating and managing bots in a Tetris-like game environment. This library offers various tools and features to build, test, and deploy bots efficiently to Botris.

## Installation

To install the library, use the following command:

```sh
pip install botris-interface
```

## Usage

### Creating a Bot

To create a bot, you need to implement the `Bot` interface provided by the library. Here is an example:

```python
from botris.bots import Bot

class CoolBot(Bot):
    async def analyze(
        self, game_state: GameState, players: List[PlayerData]
    ) -> Awaitable[List[Command]]:
        # Implement your bot logic here
        pass
```

### Running the TetrisGame

You can run the TetrisGame using the following code:

```python
from botris import TetrisGame
from botris.engine import Move

gs = TetrisGame()
gs.execute_move(Move.move_left)
```

### Connecting a Bot to the Server

To connect your bot to the server, use the following code:

```python
import asyncio
from botris import Interface

async def main():
    bot = MyBot()
    itf = Interface.create(TOKEN, ROOM_KEY, bot)
    await itf.connect()

asyncio.run(main())
```

## License

This project is licensed under the MIT License - see the [`LICENSE`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FC%3A%2FUsers%2Flunat%2FDesktop%2Fbotris-interface%2FLICENSE%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Users\lunat\Desktop\botris-interface\LICENSE") file for details.

## GitHub Repository

For more information, visit our [GitHub repository](https://github.com/lunathanael/botris-interface).

## Credits

Special thanks to [ShakTris](https://github.com/shakkar23/ShakTrisLib) providing a reliable and fast library for this project.
