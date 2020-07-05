import nonebot
from quart_auth import AuthManager, AuthUser, login_required, login_user, current_user
from quart import render_template, Blueprint
import json
import os
import httpx
import asyncio
import json
import js2py
from config import FLOWERS


bot = nonebot.get_bot()
app = bot.server_app
auth_manager = AuthManager()
auth_manager.init_app(app)
app.secret_key = 'bJmwgxzcR-Ri9ZOWjHVAxw'
# 修改web模板的位置
app.template_folder = os.path.join('web', 'templates')
# 修改静态资源位置
# app.static_folder = os.path.join('web', 'static')


@app.route('/')
@login_required
async def index():
    return "index"


@app.route('/login')
async def login():
    login_user(AuthUser(2))
    print(auth_manager.load_cookie())
    return "123"

