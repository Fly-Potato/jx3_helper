import nonebot
from os import path
import config

if __name__ == '__main__':
    nonebot.init(config)
    print(nonebot.get_bot().server_app.root_path)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'jx3', 'plugins'),
        'jx3.plugins'
    )
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'web'),
        'web'
    )
    nonebot.run()
