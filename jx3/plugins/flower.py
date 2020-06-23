from nonebot import on_command, CommandSession, logger
import httpx
from config import SERVER_KEYWORD, FLOWERS
import js2py


@on_command("flower", aliases=("花价", "花"), only_to_me=False)
async def flower(session: CommandSession):
    server_and_flower = session.get('server_and_flower', prompt="请输入要查询的服务器和花名，用空格分割，或输入web获取查询网址")
    if isinstance(server_and_flower, list):
        # 如果是个数组，表示需要获取花价
        msg = await get_flower_price(server_and_flower)
    else:
        version_info = await session.bot.get_version_info()
        url = "https://ws.xoyo.com/_daily_flower/flower/share"
        if version_info['coolq_edition'] == 'pro':

            msg = "[CQ:share,url={},title={}]".format(url, "全服花价")
        else:
            msg = "全服花价：\n{}".format(url)
    await session.send(msg)


@flower.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            await get_args(stripped_arg, session)
        return

    if not stripped_arg:
        session.pause('不能为空，请重新输入')
    await get_args(stripped_arg, session)


async def get_args(stripped_arg, session):
    args = stripped_arg.split(" ")
    server = None
    if len(args) == 1:
        if args.pop().lower() == "web":
            session.state['server_and_flower'] = "web"
        else:
            session.pause("请输入要查询的服务器和花名，用空格分割，或输入web获取查询网址")
    elif len(args) == 2:
        server_name = args[0]
        if server_name in SERVER_KEYWORD.keys():
            server_name = SERVER_KEYWORD[server_name]
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get('http://jx3gc.autoupdate.kingsoft.com/jx3hd/zhcn_hd/serverlist/serverlist.ini')
            except Exception as e:
                logger.error(e)
                await session.send(str(e))
                return
            lines = res.text.split('\n')
            for line in lines:
                _server = line.split('\t')
                if _server[1] == server_name:
                    server = _server[10]
        if not server:
            session.pause("请输入要查询的服务器和花名，用空格分割，或输入web获取查询网址")
        if args[1] in FLOWERS.keys():
            args[0] = server
            session.state['server_and_flower'] = args
        else:
            session.pause("请输入要查询的服务器和花名，用空格分割，或输入web获取查询网址")


# 获取花价
async def get_flower_price(args):
    async with httpx.AsyncClient() as client:
        server_name = args[0]
        flower_name = args[1]
        f_id = FLOWERS[flower_name]
        data = dict(serv=server_name, f_id=f_id)
        res = await client.post(url="https://ws.xoyo.com/_daily_flower/flower/get_data", data=data)
        text = ""
        for _json in js2py.eval_js(res.text):
            name = _json['type_name']
            flower_text = ""
            for f in _json['list']:
                line = f['line_name']
                price = f['price']
                update_time = f['time']
                flower_text += "分线:{} 售价:{} 更新:{}\n".format(line, price, update_time)
            text += "{}：\n{}".format(name, flower_text)
        return text
