import nonebot
from aiomysql.sa import create_engine
from config import DATABASE
import sqlalchemy as sa
from pymysql.err import InternalError


bot = nonebot.get_bot()
app = bot.server_app
engine = None
metadata = sa.MetaData()


@app.before_serving
async def init_db():

    global engine
    engine = await create_engine(loop=bot.loop, host=DATABASE['host'], port=DATABASE['port'], db=DATABASE['db'],
                                 user=DATABASE['user'], password=DATABASE['password'])
    async with engine.acquire() as conn:
        for table in tables():
            try:
                create = sa.schema.CreateTable(table)
                res = await conn.execute(create)
            except InternalError as e:
                nonebot.logger.warning(e)
        # print(res)


def tables():
    tbl = sa.Table('tbl', metadata
                   , sa.Column('id', sa.Integer, primary_key=True)
                   , sa.Column('val', sa.String(255))
                   )
    return [tbl]
