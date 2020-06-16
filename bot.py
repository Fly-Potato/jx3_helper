import nonebot
from os import path
from . import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'jx3', 'plugins'),
        'jx3.plugins'
    )
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'jx3', 'web'),
        'jx3.web'
    )
    nonebot.run()
