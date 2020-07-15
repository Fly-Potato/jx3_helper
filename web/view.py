import nonebot
from quart_auth import AuthManager, AuthUser, login_required, login_user, current_user, renew_login
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
    user = AuthUser(2)
    login_user(user)
    # print(user.auth_id)
    print(current_user.auth_id)
    renew_login()
    return "123"

