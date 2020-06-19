import nonebot
from quart_auth import AuthManager, login_required
from quart import render_template, Blueprint
import json
import os

app = nonebot.get_bot().server_app
auth_manager = AuthManager()
auth_manager.init_app(app)
app.secret_key = 'bJmwgxzcR-Ri9ZOWjHVAxw'
# 修改web模板的位置
app.template_folder = os.path.join('web', 'templates')
# 修改静态资源位置
# app.static_folder = os.path.join('web', 'static')


@app.route('/')
async def index():
    return "index"


@app.route('/login')
async def login():
    return await render_template('login.html')
