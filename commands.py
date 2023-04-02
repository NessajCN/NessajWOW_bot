# -*- coding: utf-8 -*-
import os
import requests

import botpy
from botpy import logging, BotAPI

from botpy.ext.command_util import Commands
from botpy.message import Message, DirectMessage
# from botpy.types.message import MarkdownPayload, MessageMarkdownParams

from botpy.ext.cog_yaml import read

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()


def postcommand(command: str):
    payload = {
        "auth": config["auth"],
        "command": command
    }
    try:
        response = requests.post(config["apiurl"], json=payload)
        return response.json()
    except:
        return {"success": False, "message": "Connection Error"}


@Commands(name=("/账号", "/register"))
async def register(api: BotAPI, message: Message | DirectMessage, params=None):
    _log.info(f"message: {message}\nparams:{params}")
    # 第一种用reply发送消息
    if not isinstance(message, DirectMessage) or message.direct_message != True:
        await message.reply(content="请不要在公共频道使用[/账号]指令，你也不想账号密码被广播对吧~")
        return True
    cmd = f"account create {message.author.username} {message.author.id[-6:]}"
    msg_success = f"已成功注册: \n用户名: {message.author.username}\n密码: {message.author.id[-6:]}\n请进入游戏后用在聊天栏输入 [.account set <旧密码> <新密码> <新密码>] 来修改密码。注意新密码要打两遍。"
    msg_existed = f"用户名: {message.author.username}已被注册，请不要重复注册。"

    resp = postcommand(cmd)
    if resp["success"] == True:
        await message.reply(content=msg_success)
        return True

    elif "faultString" in resp["message"] and "already exist" in resp["message"]["faultString"]:
        await message.reply(content=msg_existed)
        return True
    else:
        await message.reply(content="注册失败")
        # 第二种用api.post_message发送消息
        # await api.post_message(channel_id=message.channel_id, content=message.content, msg_id=message.id)
        return True


@Commands(name=("/帮助", "/help"))
async def help(api: BotAPI, message: Message | DirectMessage, params=None):
    _log.info(f"message: {message}\nparams:{params}")

    # 第一种用reply发送消息
    await message.reply(content="详细帮助请输入 [/info] 指令。")
    # 第二种用api.post_message发送消息
    # await api.post_message(channel_id=message.channel_id, content=message.content, msg_id=message.id)
    return True


@Commands(name=("/查询", "/info"))
async def info(api: BotAPI, message: Message | DirectMessage, params: str = None):
    _log.info(f"message: {message}\nparams:{params}")
    if params == "":
        await message.reply(content="输入以下命令查看具体信息：\n/info reg  # 注册账号\n/info client  # 客户端下载\n/info login  # 登录服务器\n/info locale  # 汉化补丁\n其中所有链接不得已用base64加密，请谅解。")
        return True
    elif params != "reg" and params != "login" and params != "client" and params != "locale":
        await message.reply(content="询问参数错误")
        return True
    else:
        with open(f"{os.path.join(os.path.dirname(__file__))}/info/{params}.md", "r", encoding="utf-8") as md:
            helpmsg = md.read()
            # replymd = MarkdownPayload(content=helpmsg)
        await message.reply(content=helpmsg)
        return True


@Commands(name=("/密码", "/pwd"))
async def pwd(api: BotAPI, message: Message, params: str = None):
    _log.info(f"message: {message}\nparams:{params}")
    if params is None or len(params.split()) != 2:
        await message.reply(content="请在 [/密码] 命令后输入旧密码和新密码，如 [/密码 123456 abcdef] 或者 [/pwd 123456 abcdefg123]")
        return True

    cmd = f"account password {message.author.username} {params}"

    # 第一种用reply发送消息
    await message.reply(content=message.content)
    # 第二种用api.post_message发送消息
    # await api.post_message(channel_id=message.channel_id, content=message.content, msg_id=message.id)
    return True
