from nonebot import on_command, CommandSession
import httpx
from json import JSONDecodeError


# 日常
@on_command('daily', aliases=('日常',))
async def daily(session: CommandSession):
    pv = session.get('pv', prompt="请输入想要查询的类型，如pve,pvp,pvx")
    report = await get_daily(pv)
    await session.send(report)


@daily.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            session.state['pv'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的类型不能为空，请重新输入')

    stripped_arg = stripped_arg.lower()

    if not stripped_arg == 'pve' and not stripped_arg == 'pvp' and not stripped_arg == 'pvx':
        session.pause('要查询的类型错误，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def get_daily(pv) -> str:
    """
    获取日常，api-剑三通
    :return:消息字符串
    """
    async with httpx.AsyncClient() as client:
        res = await client.get("https://www.jx3tong.com/?m=api&c=daily&a=daily_list")
        _json = res.json()
        try:
            state = _json['state']
        except JSONDecodeError as e:
            return e
        if state == 'success':
            update_time = _json['update_time']
            activity_data = _json['activity_data']
            pvx = activity_data[0]['activity_list']
            pve = activity_data[1]['activity_list']
            pvp = activity_data[2]['activity_list']
            text = ""
            if pv.lower() == 'pve':
                for data in pve:
                    title = data['title']
                    open_time = data['open_time']
                    if open_time == "查看简介":
                        open_time = "未知"
                    text += title+'   开放时间：'+open_time+'\n'
            elif pv.lower() == 'pvp':
                for data in pvp:
                    title = data['title']
                    open_time = data['open_time']
                    if open_time == "查看简介":
                        open_time = "未知"
                    text += title+'   开放时间：'+open_time+'\n'
            elif pv.lower() == 'pvx':
                for data in pvx:
                    title = data['title']
                    open_time = data['open_time']
                    if open_time == "查看简介":
                        open_time = "未知"
                    text += title+'   开放时间：'+open_time+'\n'
            text += update_time
            return text
        else:
            return "获取失败，state:"+state


