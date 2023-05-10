# By : @Codexun
# By : Pavan Magar

import asyncio
import json
import logging
import platform
import re
import socket
import time
import uuid
from datetime import datetime
from sys import version as pyver

from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from m8n import BOT_NAME, BOT_USERNAME
from m8n.config import BOT_NAME
from m8n.config import IMG_1

import psutil
from pyrogram import Client
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import __version__ as pytover

from m8n import (BOT_ID, BOT_NAME, SUDO_USERS, app, boottime)
from m8n import client as userbot
from m8n.utils.filters import command
from m8n.database.chats import get_served_chats
from m8n.database.sudo import get_sudoers
from m8n.database.ping import get_readable_time

def dashmarkup():
    buttons = [
        [
            InlineKeyboardButton(text="‹ الوقت ›", callback_data="UPT"),
            InlineKeyboardButton(text="‹ الرام ›", callback_data="RAT"),
        ],
        [
            InlineKeyboardButton(text="‹ الذاكرة ›", callback_data="CPT"),
            InlineKeyboardButton(text="‹ القرص ›", callback_data="DIT"),
        ],
        [InlineKeyboardButton(text="‹ رجوع ›", callback_data="settingm")],
    ]
    return f"‹ اعدادات البوت ›", buttons


stats1 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="‹ النظام ›", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="‹ البوت ›", callback_data=f"bot_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="‹ حساب المساعد ›", callback_data=f"assis_stats"
            ),
            InlineKeyboardButton(
                text="‹ التخزين ›", callback_data=f"sto_stats"
            )
        ],
       [
            InlineKeyboardButton(
                text="‹ مسح ›", callback_data=f"statsclose"
            ),
        ],
    ]
)

statsback = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="‹ رجوع ›", callback_data=f"gen_stats"
            ),
        ],
    ]
)

statswait = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="‹ اعدادات البوت ›",
                callback_data=f"wait_stats",
            )
        ]
    ]
)

async def bot_sys_stats():
    bot_uptime = int(time.time() - boottime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f"""
**• وقت التشغيل :** {get_readable_time((bot_uptime))}
**• المعالج :** {cpu}%
**• الرام :** {mem}%
**• التخزين : **{disk}%"""
    return stats




@app.on_message(command(["العدد", f"الاحصائيات"])
& ~filters.edited) 
async def gstats(_, message):
    start = datetime.now()
    try:
        await message.delete()
    except:
        pass
    uptime = await bot_sys_stats()
    response = await message.reply_photo(
        photo=f"{IMG_1}",
         caption=f"""‹ فتح الاعدادت ›"""
    )
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    smex = f"""
<u>**‹ احصائيات عامه ›**</u>
    
- البنك: `{resp} مللي ثانية`
{uptime}

**- احصل على الاحصائيات المطلوبة عن طريق الازرار ادناه**
    """
    await response.edit_text(smex, reply_markup=stats1)
    return


@app.on_callback_query(
    filters.regex(
        pattern=r"^(sys_stats|sto_stats|bot_stats|Dashboard|mongo_stats|gen_stats|assis_stats|wait_stats|stats_close)$"
    )
)
async def stats_markup(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    if command == "sys_stats":
        await CallbackQuery.edit_message_text(
            "‹ اعدادات البوت ›", reply_markup=statswait
        )
        sc = platform.system()
        arch = platform.machine()
        ram = (
            str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        )
        bot_uptime = int(time.time() - boottime)
        uptime = f"{get_readable_time((bot_uptime))}"
        smex = f"""
<u>**‹ احصائيات النظام ›**</u>

**• الوقت :** {uptime}
**• نظام التشغيل :** متصل
**• الاستضافة :** {sc}
**• البناء :** {arch}
**• الرام :** {ram}
**• نسخة التشغيل :** {pytover.__version__}
**• نسخة بايثون :** {pyver.split()[0]}
**• نسخة بايروجرام :** {pyrover}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=statsback)
    if command == "sto_stats":
        await CallbackQuery.edit_message_text(
            "‹ اعدادات البوت  ›", reply_markup=statswait
        )
        hdd = psutil.disk_usage("/")
        total = hdd.total / (1024.0 ** 3)
        total = str(total)
        used = hdd.used / (1024.0 ** 3)
        used = str(used)
        free = hdd.free / (1024.0 ** 3)
        free = str(free)
        smex = f"""
<u>**‹ احصائيات التخزين ›**</u>

**• التخزين المتوفر :** {total[:4]} GiB 
**• التخزين المستخدم :** {used[:4]} GiB
**• التخزين المتبقي :** {free[:4]} GiB"""
        await CallbackQuery.edit_message_text(smex, reply_markup=statsback)
    if command == "bot_stats":
        await CallbackQuery.edit_message_text(
            "‹ اعدادات البوت ›", reply_markup=statswait
        )
        served_chats = []
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
        sudoers = await get_sudoers()
        modules_loaded = "20"
        j = 0
        for count, user_id in enumerate(sudoers, 0):
            try:
                user = await app.get_users(user_id)
                j += 1
            except Exception:
                continue
        smex = f"""
<u>**‹ احصائيات البوت الرسمية ›**</u>

**• الوحدات :** {modules_loaded}
**• عدد المطورين :** {j}
**• عدد الكروبات :** {len(served_chats)}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=statsback)
    if command == "assis_stats":
        await CallbackQuery.edit_message_text(
            "‹ اعدادات البوت ›", reply_markup=statswait
        )
        groups_ub = channels_ub = bots_ub = privates_ub = total_ub = 0
        async for i in userbot.iter_dialogs():
            t = i.chat.type
            total_ub += 1
            if t in ["supergroup", "group"]:
                groups_ub += 1
            elif t == "channel":
                channels_ub += 1
            elif t == "bot":
                bots_ub += 1
            elif t == "private":
                privates_ub += 1

        smex = f"""
<u>**‹ احصائيات حساب المساعد ›**</u>

**• الخاص :** {total_ub}
**• الكروبات :** {groups_ub} 
**• القنوات :** {channels_ub} 
**• البوتات :** {bots_ub}
**• المستخدمين :** {privates_ub}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=statsback)
    if command == "gen_stats":
        start = datetime.now()
        uptime = await bot_sys_stats()
        end = datetime.now()
        resp = (end - start).microseconds / 1000
        smex = f"""
<u>**‹ اعدادات البوت  ›**</u>

**- البنك :** `{resp} مللي ثانية`
{uptime}

**- يمكنك الحصول على الاحصائيات عن طريق الازرار ادناه**"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats1)
    if command == "wait_stats":
        await CallbackQuery.answer()

@app.on_callback_query(filters.regex("statsclose"))
async def statsclose(_, query: CallbackQuery):
   await query.message.delete()
