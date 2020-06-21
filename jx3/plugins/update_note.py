from nonebot import on_command, CommandSession, get_bot


@on_command('更新日志', aliases=('更新说明', '更新公告'), only_to_me=False)
async def update_note(session: CommandSession):
    version_info = await session.bot.get_version_info()
    if version_info['coolq_edition'] == 'pro':
        msg = "[CQ:share,url={},title={}]".format("https://jx3.xoyo.com/launcher/update/latest.html", "剑网三更新日志")
    else:
        msg = "更新日志：\n {}".format("https://jx3.xoyo.com/launcher/update/latest.html")
    await session.send(msg)
