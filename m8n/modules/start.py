import asyncio

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, UserNotParticipant
from pytgcalls import (__version__ as pytover)

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from m8n.utils.filters import command


from m8n.config import BOT_USERNAME
from m8n.config import START_PIC
from m8n.config import BOT_NAME
from m8n.config import UPDATE
from m8n.config import OWNER_USERNAME



@Client.on_message(command("/start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{START_PIC}",
        caption=f""" ‹ مرحبا بك عزيزي في بوت **{BOT_NAME}**
        
- اضغط على زر ‹ الاوامر › لمعرفة الأوامر ›

- اضغط على زر ‹ الاعدادات › لمعرفة الاعدادات ›""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "‹ الاعدادات ›", callback_data="cbabout"),
                ],
                [
                    InlineKeyboardButton(
                        "‹ الاوامر ›", callback_data="cbevery")
                ],
                [
                    InlineKeyboardButton(
                        "‹ اضفني الى مجموعتك ›", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ]
           ]
        ),
    )



@Client.on_message(command(["المطور", f"مطور"]) & filters.group & ~filters.edited)
async def gcstart(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://te.legra.ph/file/5fdd8da2461c05d893189.jpg",
        caption=f"- مطور البوت . \n\n - قناة المطور @{UPDATE}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("- المطور .", url=f"https://t.me/{OWNER_USERNAME}")
                ]
            ]
        ),
    )


