from nonebot import on_command, CommandSession
import httpx


@on_command('客服公告', only_to_me=False)
async def kefu(session: CommandSession):
    async with httpx.AsyncClient() as client:
        res = await client.get("https://jx3.xoyo.com/client/v3_kefu.txt")
        await session.send(res.text)
