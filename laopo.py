from hoshino import Service, priv, config
from hoshino.typing import CQEvent
import httpx
import hashlib
import base64
import os
import json
import datetime
from random import choice

sv = Service(
    name="今日老婆",  # 功能名
    visible=True,  # 可见性
    enable_on_default=True,  # 默认启用
    bundle="娱乐",  # 分组归类
    help_="发送【今日老婆】随机抓取群友作为老婆",  # 帮助说明

)

def get_member_list(all_list):
    id_list = []
    for member_list in all_list:
        id_list.append(member_list['user_id'])
    return id_list

async def download_avatar(user_id: str) -> bytes:
    url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
    data = await download_url(url)
    if not data or hashlib.md5(data).hexdigest() == "acef72340ac0e914090bd35799f5594e":
        url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=100"
        data = await download_url(url)
    return data

async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url)
                if resp.status_code != 200:
                    continue
                return resp.content
            except Exception as e:
                print(f"Error downloading {url}, retry {i}/3: {str(e)}")

async def get_wife_info(member_info,qqid):  
    img = await download_avatar(qqid)
    base64_str = base64.b64encode(img).decode()
    avatar =  'base64://' + base64_str
    member_name = (member_info["card"] or member_info["nickname"])
    result = f'''\n你今天的群友老婆是:
[CQ:image,file={avatar}]
{member_name}({qqid})'''
    return result

def load_group_config(group_id: str) -> int:
    filename = os.path.join(os.path.dirname(__file__), 'config', f'{group_id}.json')
    try:
        with open(filename, encoding='utf8') as f:
            config = json.load(f)
            return config
    except:
        return None

def write_group_config(group_id: str,link_id:str,wife_id:str,date:str,config) -> int:
    config_file = os.path.join(os.path.dirname(__file__), 'config', f'{group_id}.json')
    if config != None:    
        config[link_id] = [wife_id,date]
    else:
        config = {link_id:[wife_id,date]}
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False)

@sv.on_fullmatch('今日老婆')
async def dailywife(bot, ev: CQEvent):
    groupid = ev.group_id
    user_id = ev.user_id
    bot_id = ev.self_id
    wife_id = None
    today = str(datetime.date.today())
    config = load_group_config(groupid)

    if priv.check_priv(ev, priv.SUPERUSER):
        wife_id = bot_id
    elif config != None:
        if str(user_id) in list(config):
            if config[str(user_id)][1] == today:
                wife_id = config[str(user_id)][0]
            else:
                del config[str(user_id)]
    
    if wife_id is None:
        all_list = await bot.get_group_member_list(group_id=groupid)
        id_list = get_member_list(all_list)
        id_list.remove(bot_id)
        id_list.remove(user_id)
        if config != None:
            for record_id in list(config):
                if config[record_id][1] != today:
                    del config[record_id]
                else:
                    try:
                        id_list.remove(int(config[record_id][0]))
                    except:
                        del config[record_id]
        wife_id = choice(id_list)

    write_group_config(groupid,user_id,wife_id,today,config)
    member_info = await bot.get_group_member_info(group_id=groupid,user_id=wife_id)
    result = await get_wife_info(member_info,wife_id)   
    await bot.send(ev,result,at_sender=True)
    
