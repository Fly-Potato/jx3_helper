import nonebot
from aiomysql.sa import create_engine
import aiomysql
from config import DATABASE
import sqlalchemy as sa
from aiomysql.sa.connection import SAConnection
from pymysql.err import InternalError
import quart_auth


bot = nonebot.get_bot()
app = bot.server_app
pool = None


# 初始化数据库连接，并创建表格
@app.before_serving
async def init_db():

    global pool
    pool = await aiomysql.create_pool(host=DATABASE['host'], port=DATABASE['port'],
                                      user=DATABASE['user'], password=DATABASE['password'],
                                      db=DATABASE['db'], loop=bot.loop, autocommit=False)
    async with pool.acquire() as conn:
        bot.logger.debug("mysql version： {}".format(conn.get_server_info()))
        await User.init_db(conn)

    # engine = await create_engine(loop=bot.loop, host=DATABASE['host'], port=DATABASE['port'], db=DATABASE['db'],
    #                              user=DATABASE['user'], password=DATABASE['password'])
    # async with engine.acquire() as conn:
    #     tables = get_tables()
    #     for table in tables:
    #         try:
    #             print(type(conn))
    #             create_table = sa.schema.CreateTable(table)
    #             await conn.execute(create_table)
    #
    #         except InternalError as e:
    #             nonebot.logger.warning(e)


# # 创建用户
# async def create_user():
#     async with engine.acquire() as conn:
#         conn.execute()
#         # print(res)


# 创建数据库
async def _create_dbs():
    pass


class User:
    def __init__(self):
        super(User, self).__init__()

    @classmethod
    async def init_db(cls, conn: aiomysql.connection.Connection):
        cur = await conn.cursor()
        await cur.execute("show tables")
        bot.logger.info("create model user...")
        r = await cur.execute("""
        CREATE TABLE IF NOT EXISTS `user`(
           `id` INT UNSIGNED AUTO_INCREMENT,
           `qq` VARCHAR(100) NOT NULL,
           `password` VARCHAR(40) NOT NULL,
           `create_time` DATE NOT NULL,
           PRIMARY KEY ( `id` )
        )
        """)

    @classmethod
    async def create_user(cls):
        pass
