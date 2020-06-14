from nonebot import on_command, CommandSession
import httpx


@on_command('dbm', aliases=('DBM',))
async def dbm(session: CommandSession):
    report = await get_dbm_of_author()
    # 向用户发送DBM的作者
    await session.send(report)


async def get_dbm_of_author() -> str:
    async with httpx.AsyncClient() as client:
        res = await client.get("https://server.jx3box.com/post/list?type=jx3dat&per=20&subtype=1&page=1")
        dbm_info_list = res.json()['data']['list']
        for dbm_info in dbm_info_list:
            print(dbm_info['author']['name'])

    return 'dbm列表'
