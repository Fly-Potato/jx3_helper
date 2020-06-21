from nonebot import on_command, CommandSession, get_bot
from config import BASE_DIR
import os.path
import httpx
import asyncio


bot = get_bot()


@on_command('server', aliases=("开服", "开服查询"))
async def server_state(session: CommandSession):
    # server_list_path = os.path.join(BASE_DIR, 'jx3', 'server_list.txt')
    server_name = session.get('server_name', prompt="请输入想要查询的服务器名称")
    report = await check_server(server_name)
    if report:
        await session.send(report)
    else:
        await session.send()


@server_state.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，作为参数传入
            session.state['pv'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的服务器名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的服务器不能为空，请重新输入')

    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def check_server(server_name):
    async with httpx.AsyncClient() as client:
        res = await client.get('http://jx3gc.autoupdate.kingsoft.com/jx3hd/zhcn_hd/serverlist/serverlist.ini')
        lines = res.text.split('\n')
        # app.logger.debug(lines)
        for line in lines:
            _server = line.split('\t')
            # app.logger.debug(_server)
            if _server[1].find(server_name) >= 0:
                ip = _server[3]
                port = int(_server[4])
                try:
                    # 设置协程超时
                    await asyncio.wait_for(asyncio.open_connection(host=ip, port=port, loop=bot.loop), 3.0,
                                           loop=bot.loop)
                    return _server[1]+"已开服！"
                except asyncio.exceptions.TimeoutError as e:
                    return _server[1] + "维护中！"
                # try:
                #     socket = await asyncio.open_connection(host=ip, port=111, loop=bot.loop)
                #     if socket:
                #         return _server[1]+"已开服！"
                # except OSError as e:
                #     return _server[1] + "维护中！"
        return "服务器{}未找到".format(server_name)
