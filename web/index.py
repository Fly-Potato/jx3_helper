import nonebot
from quart_auth import AuthManager, login_required
from quart import render_template
import json

app = nonebot.get_bot().server_app
auth_manager = AuthManager()
auth_manager.init_app(app)
app.secret_key = 'bJmwgxzcR-Ri9ZOWjHVAxw'


@app.route('/')
@login_required
async def index():
    return "index"


@app.route('/login')
async def login():
    return await render_template('login.html')

