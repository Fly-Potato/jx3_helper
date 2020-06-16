import nonebot

bot = nonebot.get_bot()


@bot.server_app.route('/')
def index():
    return "index"
