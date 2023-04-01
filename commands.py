# -*- coding: utf-8 -*-
import os
import requests

import botpy
from botpy import logging, BotAPI

from botpy.ext.command_util import Commands
from botpy.message import Message
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


@Commands(name=("/注册", "/register"))
async def register(api: BotAPI, message: Message, params=None):
    _log.info(f"message: {message}\nparams:{params}")
    # 第一种用reply发送消息

    cmd = f"account create {message.author.username} {message.author.id[-6:]}"
    msg_success = f"已成功注册: \n用户名: {message.author.username}\n密码: {message.author.id[-6:]}\n请尽快使用 [/密码 <你的新密码>] 或 [/pwd <你的新密码>] （不带中括号）来修改密码"
    msg_existed = f"用户名: {message.author.username}已被注册，请不要重复注册。"

    resp = postcommand(cmd)
    if resp["success"] == True:
        await message.reply(content=msg_success)
    elif "faultString" in resp["message"] and "already exist" in resp["message"]["faultString"]:
        await message.reply(msg_existed)
    await message.reply(content="注册失败")
    # 第二种用api.post_message发送消息
    # await api.post_message(channel_id=message.channel_id, content=message.content, msg_id=message.id)
    return True


@Commands(name=("/帮助", "/help"))
async def help(api: BotAPI, message: Message, params=None):
    _log.info(f"message: {message}\nparams:{params}")
    # 第一种用reply发送消息
    await message.reply(content=message.content)
    # 第二种用api.post_message发送消息
    # await api.post_message(channel_id=message.channel_id, content=message.content, msg_id=message.id)
    return True


@Commands(name=("/查询", "/info"))
async def info(api: BotAPI, message: Message, params=None):
    _log.info(f"message: {message}\nparams:{params}")
    # 第一种用reply发送消息
    await message.reply(content=message.content)
    # 第二种用api.post_message发送消息
    # await api.post_message(channel_id=message.channel_id, content=message.content, msg_id=message.id)
    return True


@Commands(name=("/密码", "/pwd"))
async def pwd(api: BotAPI, message: Message, params=None):
    _log.info(f"message: {message}\nparams:{params}")
    # 第一种用reply发送消息
    await message.reply(content=message.content)
    # 第二种用api.post_message发送消息
    # await api.post_message(channel_id=message.channel_id, content=message.content, msg_id=message.id)
    return True
