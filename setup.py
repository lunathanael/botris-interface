# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botris',
 'botris.bots',
 'botris.bots.bot',
 'botris.bots.randombot',
 'botris.engine',
 'botris.interface']

package_data = \
{'': ['*'], 'botris': ['test_cython/*']}

install_requires = \
['colorama>=0.4.6,<0.5.0',
 'pillow>=10.4.0,<11.0.0',
 'protobuf>=5.27.3,<6.0.0',
 'pybind11>=2.13.3,<3.0.0',
 'pydantic>=2.8.2,<3.0.0',
 'setuptools>=72.2.0,<73.0.0',
 'websockets>=12.0,<13.0']

setup_kwargs = {
    'name': 'botris-interface',
    'version': '0.1.21',
    'description': 'A performant library designed for creating and managing bots in a Tetris-like game environment. This library offers various tools and features to build, test, and deploy bots efficiently to Botris.',
    'long_description': '# botris-interface\n\n[![GitHub license](https://img.shields.io/github/license/lunathanael/botris-interface)](https://github.com/lunathanael/botris-interface/blob/main/LICENSE)\n[![GitHub issues](https://img.shields.io/github/issues/lunathanael/botris-interface)](https://github.com/lunathanael/botris-interface/issues)\n[![GitHub stars](https://img.shields.io/github/stars/lunathanael/botris-interface?style=social)](https://github.com/lunathanael/botris-interface/stargazers)\n[![GitHub forks](https://img.shields.io/github/forks/lunathanael/botris-interface?style=social)](https://github.com/lunathanael/botris-interface/network/members)\n\nbotris-interface is a performant library designed for creating and managing bots in a Tetris-like game environment. This library offers various tools and features to build, test, and deploy bots efficiently to Botris.\n\n## Installation\n\nTo install the library, use the following command:\n\n```sh\npip install botris-interface\n```\n\n## Usage\n\n### Creating a Bot\n\nTo create a bot, you need to implement the `Bot` interface provided by the library. Here is an example:\n\n```python\nfrom botris.bots import Bot\n\nclass CoolBot(Bot):\n    async def analyze(\n        self, game_state: GameState, players: List[PlayerData]\n    ) -> Awaitable[List[Command]]:\n        # Implement your bot logic here\n        pass\n```\n\n### Running the TetrisGame\n\nYou can run the TetrisGame using the following code:\n\n```python\nfrom botris import TetrisGame\nfrom botris.engine import Move\n\ngs = TetrisGame()\ngs.execute_move(Move.move_left)\n```\n\n### Connecting a Bot to the Server\n\nTo connect your bot to the server, use the following code:\n\n```python\nimport asyncio\nfrom botris import Interface\n\nasync def main():\n    bot = MyBot()\n    itf = Interface.create(TOKEN, ROOM_KEY, bot)\n    await itf.connect()\n\nasyncio.run(main())\n```\n\n## License\n\nThis project is licensed under the MIT License - see the [`LICENSE`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FC%3A%2FUsers%2Flunat%2FDesktop%2Fbotris-interface%2FLICENSE%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\\Users\\lunat\\Desktop\\botris-interface\\LICENSE") file for details.\n\n## GitHub Repository\n\nFor more information, visit our [GitHub repository](https://github.com/lunathanael/botris-interface).',
    'author': 'Nathanael Lu',
    'author_email': 'info@lunathanael.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
