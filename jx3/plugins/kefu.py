from nonebot import on_command, CommandSession, logger
import httpx


@on_command('客服公告', only_to_me=False)
async def kefu(session: CommandSession):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get("https://jx3.xoyo.com/client/v3_kefu.txt")
            logger.info(await session.send(res.text, ignore_failure=False))
        except Exception as e:
            logger.error(e)
            await session.send(e)

