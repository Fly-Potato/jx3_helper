import nonebot
from aiomysql.sa import create_engine
from config import DATABASE
import sqlalchemy as sa
from pymysql.err import InternalError
from .tables import *


bot = nonebot.get_bot()
app = bot.server_app
engine = None


# 初始化数据库连接，并创建表格
@app.before_serving
async def init_db():

    global engine
    engine = await create_engine(loop=bot.loop, host=DATABASE['host'], port=DATABASE['port'], db=DATABASE['db'],
                                 user=DATABASE['user'], password=DATABASE['password'])
    async with engine.acquire() as conn:
        tables = get_tables()
        for table in tables:
            try:
                create_table = sa.schema.CreateTable(table)
                await conn.execute(create_table)
            except InternalError as e:
                nonebot.logger.warning(e)


# 创建用户
async def create_user():
    async with engine.acquire() as conn:
        conn.execute()
        # print(res)
