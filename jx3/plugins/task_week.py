from nonebot import on_command, CommandSession, logger
import httpx


@on_command('周常', only_to_me=False)
async def task_week(session: CommandSession):
    report = await get_task_week()
    logger.debug("周常 send msg..")
    await session.send(report)


async def get_task_week():
    async with httpx.AsyncClient() as client:
        res = await client.get('https://www.jx3tong.com/?m=api&c=daily&a=daily_list')
        _json = res.json()
        update_time = _json["update_time"]
        _json = _json['activity_data'][1]['activity_list']
        task_list = ""
        for j in _json:
            if "武林通鉴" in j['title']:
                res = await client.get('https://www.jx3tong.com/?m=api&c=daily&a=daily_detail&daily_id='+j['id'])
                j = res.json()
                task_list += "{}: {}\n".format(j["detail"]["title"], j["detail"]["join_method"].replace("\n\n", "\n"))
        task_list += "更新日期：{}".format(update_time)
        return task_list
