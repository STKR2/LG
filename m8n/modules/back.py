import aiofiles
import ffmpeg
import asyncio
import os
import shutil
import psutil
import subprocess
import requests
import aiohttp
import yt_dlp
import aiohttp
import random

from os import path
from typing import Union
from asyncio import QueueEmpty
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from PIL import ImageGrab
from typing import Callable

from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

from youtube_search import YoutubeSearch

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    Voice,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden


from m8n.tgcalls import calls, queues
from m8n.tgcalls.youtube import download
from m8n.tgcalls import convert as cconvert
from m8n.tgcalls.calls import client as ASS_ACC
from m8n.database.queue import (
    get_active_chats,
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)

from m8n import BOT_NAME, BOT_USERNAME
from m8n import app
import m8n.tgcalls
from m8n.tgcalls import youtube
from m8n.config import (
    DURATION_LIMIT,
    que,
    SUDO_USERS,
    BOT_ID,
    ASSNAME,
    ASSUSERNAME,
    ASSID,
    START_PIC,
    SUPPORT,
    UPDATE,
    BOT_NAME,
    BOT_USERNAME,
)
from m8n.utils.filters import command
from m8n.utils.decorators import errors, sudo_users_only
from m8n.utils.administrator import adminsOnly
from m8n.utils.errors import DurationLimitError
from m8n.utils.gets import get_url, get_file_name
from m8n.modules.admins import member_permissions


def others_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"resumevc"),
            InlineKeyboardButton(text="II", callback_data=f"pausevc"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"skipvc"),
            InlineKeyboardButton(text="▢", callback_data=f"stopvc"),
        ],[
            InlineKeyboardButton(text="Manage", callback_data=f"cls"),
        ],
        
    ]
    return buttons


fifth_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200% تم", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="‹ رجوع ›", callback_data=f"cbmenu"),
        ],
    ]
)

fourth_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150% تم", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="‹ رجوع ›", callback_data=f"cbmenu"),
        ],
    ]
)

third_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100% تم", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="‹ رجوع ›", callback_data=f"cbmenu"),
        ],
    ]
)

second_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20%", callback_data="first"),
            InlineKeyboardButton("50% تم", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="‹ رجوع ›", callback_data=f"cbmenu"),
        ],
    ]
)

first_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("20% تم", callback_data="first"),
            InlineKeyboardButton("50%", callback_data="second"),
            
        ],[
            
            InlineKeyboardButton("100%", callback_data="third"),
            InlineKeyboardButton("150%", callback_data="fourth"),
            
        ],[
            
            InlineKeyboardButton("200%", callback_data="fifth"),
            
        ],[
            InlineKeyboardButton(text="‹ رجوع ›", callback_data=f"cbmenu"),
        ],
    ]
)
highquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("‹ ضعيف ›", callback_data="low"),],
         [   InlineKeyboardButton("‹ متوسط ›", callback_data="medium"),
            
        ],[   InlineKeyboardButton("‹ عالي تم ›", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="‹ رجوع ›", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="‹ تنظيف ›", callback_data=f"cls"),
        ],
    ]
)
lowquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("‹ ضعيف تم ›", callback_data="low"),],
         [   InlineKeyboardButton("‹ متوسط ›", callback_data="medium"),
            
        ],[   InlineKeyboardButton("‹ عالي ›", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="‹ رجوع ›", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="‹ تنظيف ›", callback_data=f"cls"),
        ],
    ]
)
mediumquality_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("‹ ضعيف ›", callback_data="low"),],
         [   InlineKeyboardButton("‹ متوسط تم›", callback_data="medium"),
            
        ],[   InlineKeyboardButton("‹ عالي ›", callback_data="high"),
            
        ],[
            InlineKeyboardButton(text="‹ رجوع ›", callback_data=f"cbmenu"),
            InlineKeyboardButton(text="‹ تنظيف ›", callback_data=f"cls"),
        ],
    ]
)

dbclean_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("يب متأكد .", callback_data="cleandb"),],
        [    InlineKeyboardButton("لا يمعود اشاقة .", callback_data="cbmenu"),
            
        ],[
            InlineKeyboardButton(text="‹ رجوع ›", callback_data=f"cbmenu"),
        ],
    ]
)
menu_keyboard = InlineKeyboardMarkup(
    [
        [
            
            InlineKeyboardButton("▷", callback_data="resumevc"),
            InlineKeyboardButton("II", callback_data="pausevc"),
            InlineKeyboardButton("‣‣I", callback_data="skipvc"),
            InlineKeyboardButton("▢", callback_data="stopvc"),
            
        ],[
            InlineKeyboardButton(text="‹ الصوت ›", callback_data=f"fifth"),
             InlineKeyboardButton(text="‹ الجودة ›", callback_data=f"high"),
        ],[
            InlineKeyboardButton(text="‹ اطفاء عام ›", callback_data=f"dbconfirm"),
             InlineKeyboardButton(text="‹ الدعم ›", callback_data=f"nonabout"),
        ],[
             InlineKeyboardButton(text="‹ تنظيف ›", callback_data=f"cls"),
        ],
    ]
)


@Client.on_callback_query(filters.regex("skipvc"))
async def skipvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    if await is_active_chat(chat_id):
            user_id = CallbackQuery.from_user.id
            await remove_active_chat(chat_id)
            user_name = CallbackQuery.from_user.first_name
            rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
            await CallbackQuery.answer()
            await CallbackQuery.message.reply(
                f"""
**- تم تخطي الاغنية بواسطة** {rpk}
• لايوجد شي قيد التشغيل 
`- تم مغادرة حساب المساعد`
"""
            )
            await calls.pytgcalls.leave_group_call(chat_id)
            return
            await CallbackQuery.answer("- تم بنجاح !", show_alert=True)     

@Client.on_callback_query(filters.regex("pausevc"))
async def pausevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await music_off(chat_id)
            await calls.pytgcalls.pause_stream(chat_id)
            await CallbackQuery.answer("- تم ايقاف الموسيقى مؤقتا .", show_alert=True)
            
        else:
            await CallbackQuery.answer(f"- ماكو شي مشتغل شبيك رحمه لدينك", show_alert=True)
            return
    else:
        await CallbackQuery.answer(f"- ماكو شي مشتغل شبيك رحمه لدينك !", show_alert=True)


@Client.on_callback_query(filters.regex("resumevc"))
async def resumevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await CallbackQuery.answer(
                "- ليش هوه اكو شي مشتغل ؟.",
                show_alert=True,
            )
            return
        else:
            await music_on(chat_id)
            await calls.pytgcalls.resume_stream(chat_id)
            await CallbackQuery.answer(" - تم إستئناف التشغيل.", show_alert=True)
            
    else:
        await CallbackQuery.answer(f"- والعباس ماكو شي مشتغل", show_alert=True)


@Client.on_callback_query(filters.regex("stopvc"))
async def stopvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        
        try:
            await calls.pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await remove_active_chat(chat_id)
        await CallbackQuery.answer("- تم انهاء التشغيل بنجاح.", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await CallbackQuery.message.reply(f"**• تم الايقاف بواسطة {rpk}.**")
    else:
        await CallbackQuery.answer(f"- ماكو شي مشتغل لتخليني افشر", show_alert=True)

@Client.on_callback_query(filters.regex("cleandb"))
async def cleandb(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        
        try:
            await calls.pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await remove_active_chat(chat_id)
        await CallbackQuery.answer("- تم تنظيف التشغيل !", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await CallbackQuery.edit_message_text(
        f" __- تم التنظيف بنجاح__\n│\n╰ بواسطة {rpk}",
        reply_markup=InlineKeyboardMarkup(
            [
            [InlineKeyboardButton("‹ تنظيف ›", callback_data="cls")]])
        
    )
    else:
        await CallbackQuery.answer(f"- لتكفرني ماكو شي مشتغل .", show_alert=True)

@Client.on_callback_query(filters.regex(pattern=r"^(cls)$"))
async def closed(_, query: CallbackQuery):
    from_user = query.from_user
    permissions = await member_permissions(query.message.chat.id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await query.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    await query.message.delete()

@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("- ماتكدر تبعبص انت مجهول !\n\n- ارجع ادمن وتدلل")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›", show_alert=True)
    chat_id = query.message.chat.id
    if is_music_playing(chat_id):
          await query.edit_message_text(
              f"**‹ مرحبا بك في قائمة الاعدادات ›\n\n- أسم ڪࢪۅبي : {query.message.chat.title}.\n- أيدي ڪࢪۅبي : {query.message.chat.id}\n\n**- يمكنك التحكم في الازرار ولاكن كن حذراً .**",

              reply_markup=menu_keyboard
         )
    else:
        await query.answer("- ماكو شي مشتغل رحمه لدينك", show_alert=True)



@Client.on_callback_query(filters.regex("high"))
async def high(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("- تم ارتفاع الصوت الى عالي!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**‹ يمكنك التحكم في اعدادات جودة الصوت ›**\n\n- لاتنسى كن حذراً .",
        reply_markup=highquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"- ماكو شي مشتغل حب .", show_alert=True)


@Client.on_callback_query(filters.regex("low"))
async def low(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("- تم الان يعمل بصوت ضعيف!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**‹ يمكنك التحكم في اعدادات جودة الصوت ›**\n\n- لاتنسى كن حذراً",
        reply_markup=lowquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"- ماكو شي مشتغل حب.", show_alert=True)

@Client.on_callback_query(filters.regex("medium"))
async def medium(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("- تم يعمل الان متوسط !", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**‹ يمكنك التحكم في اعدادات جودة الصوت ›**\n\n- لاتنسى كن حذراً .",
        reply_markup=mediumquality_keyboard
    )
    else:
        await CallbackQuery.answer(f"- ماكو شي مشتغل حب .", show_alert=True)

@Client.on_callback_query(filters.regex("fifth"))
async def fifth(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("- الصوت تلقائيا 200 ", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**‹ يمكنك التحكم في اعدادات حجم الصوت ›**\n\n- عند استخدامك لحجم الصوت عليك رفع حساب المساعد كمشرف هنا",
        reply_markup=fifth_keyboard
    )
    else:
        await CallbackQuery.answer(f"- ماكو شي مشتغل حب", show_alert=True)

@Client.on_callback_query(filters.regex("fourth"))
async def fourth(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("تم وسويت الصوت 150 !", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**‹ يمكنك التحكم في اعدادات حجمه الصوت ›**\n\n- عند استخدامك لحجم الصوت عليك رفع حساب المساعد كمشرف هنا",
        reply_markup=fourth_keyboard
    )
    else:
        await CallbackQuery.answer(f"- ماكو شي مشتغل حب .", show_alert=True)

@Client.on_callback_query(filters.regex("third"))
async def third(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("تم وسويت الصوت 100", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**‹ يمكنك التحكم في اعدادات حجم الصوت ›**\n\n- عند استخدامك لحجم الصوت عليك رفع حساب المساعد كمشرف هنا",
        reply_markup=third_keyboard
    )
    else:
        await CallbackQuery.answer(f"- ماكو شي مشتغل حب", show_alert=True)


@Client.on_callback_query(filters.regex("second"))
async def second(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("تم وسويت الصوت 50", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**‹ يمكنك التحكم في اعدادات حجم الصوت ›**\n\n- عند استخدامك لحجم الصوت عليك رفع حساب المساعد كمشرف هنا.",
        reply_markup=second_keyboard
    )
    else:
        await CallbackQuery.answer(f"- ماكو شي مشتغل حب.", show_alert=True)


@Client.on_callback_query(filters.regex("first"))
async def first(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
            
        await CallbackQuery.answer("- تم وسويت الصوت 20!", show_alert=True)
        await CallbackQuery.edit_message_text(
        f"**‹ يمكنك التحكم في اعدادات حجم الصوت ›**\n\n- عند استخدامك لحجم الصوت عليك رفع حساب المساعد كمشرف هنا.",
        reply_markup=first_keyboard
    )
    else:
        await CallbackQuery.answer(f"- ماكو شي مشتغل حب .", show_alert=True)

@Client.on_callback_query(filters.regex("nonabout"))
async def nonabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**‹ مرحبا بك في قسم الدعم الخاص بالمساعدة › \n\n - يمكنك التواصل مع المطورين عن طريق الازرار ادناه**""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton("‹ الدعم ›", url=f"https://t.me/{SUPPORT}"),
                    InlineKeyboardButton("‹ المطور ›", url=f"https://t.me/{UPDATE}")
                ],
              [InlineKeyboardButton("‹ رجوع ›", callback_data="cbmenu")]]
        ),
    )


@Client.on_callback_query(filters.regex("dbconfirm"))
async def dbconfirm(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("- انت مجهول !\n\n- ارجع ادمن وتدلل .")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("‹ امشي عليك سيد لوط لتبعبص اذا ماعندك مشرف ›", show_alert=True)
    chat_id = query.message.chat.id
    if is_music_playing(chat_id):
          await query.edit_message_text(
              f"**‹ مرحبا بك في قسم الاطفاء العام ›**\n\n- يرجى ملاحظة انَ سيتم اطفاء جميع الاغاني هنا {query.message.chat.title} حتى قوائم الانتضار **",

              reply_markup=dbclean_keyboard
         )
    else:
        await query.answer("- ماكو شي مشتغل حب", show_alert=True)

@Client.on_callback_query(filters.regex("speed"))
async def speed(_, query: CallbackQuery):
    await query.answer(
            "🌟 SPEED OF THE SERVER :\n• 4.4568 ms\n• 1264.0 ms\n• 98.20 ms\n• 00.01 ms",
            show_alert=True,
        )
