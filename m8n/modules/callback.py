from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from m8n.config import BOT_USERNAME
from m8n.config import START_PIC
from m8n.config import OWNER_ID
from m8n.config import ASSUSERNAME
from m8n.config import UPDATE
from m8n.config import SUPPORT
from m8n.config import OWNER_USERNAME
from m8n.config import BOT_NAME


@Client.on_callback_query(filters.regex("cbhome"))
async def cbhome(_, query: CallbackQuery):
    await query.edit_message_text(
        f""" ‹ مرحبا بك عزيزي في بوت **{BOT_NAME}**

- اضغط على زر ‹ الاوامر › لمعرفة الأوامر ›

 - اضغط على زر ‹ الاعدادات › لمعرفة المطورين ›""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "‹ الاعدادات ›", callback_data="cbabout"),
                    InlineKeyboardButton(
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


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds_set(_, query: CallbackQuery):
        await query.answer("commands menu")
        await query.edit_message_text(
        f"""‹ مرحا بك في قسم الاوامر  › [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) 

- يمكنك معرفة الاوامر عن طريق الازرار أدناه -""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("‹ اوامر المطورين ›", callback_data="cbsudo"),
                ],[
                    InlineKeyboardButton("Everyone", callback_data="cbevery"),
                    InlineKeyboardButton("‹ اوامر المشرفين ›", callback_data="cbadmins"),
                ],[
                    InlineKeyboardButton("‹ رجوع ›", callback_data="cbhome")
                ],
            ]
        ),
    ) 


# Commands for Everyone !!
@Client.on_callback_query(filters.regex("cbevery"))
async def all_set(_, query: CallbackQuery):
    await query.answer("Everyone menu")
    await query.edit_message_text(
    f"""• /play (song name) or (YT link)
- plays the song in voice chat of your group 

• /song (song name) or (YT link)
- Downloads song in audio File 

• /tgm or /telegraph
- generate the link of given media

• /info 
- show all the information about a given user

• /search or /yt
- search link of the given song

• /ping
- Shows the ping message

• @botusername <query> 
- Get youtube url by inline mode""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton(
                        "‹ اوامر المشرفين ›", callback_data="cbadmins"),
                    InlineKeyboardButton(
                        "‹ اوامر المطورين ›", callback_data="cbsudo")
                ],
              [InlineKeyboardButton("‹ رجوع ›", callback_data="cbhome")]]
        ),
    )


# Commands for SudoUsers
@Client.on_callback_query(filters.regex("cbsudo"))
async def sudo_set(_, query: CallbackQuery):
    await query.answer("sudo menu")
    await query.edit_message_text(
    f"""• /restart 
- restarts the bot in Heroku 

• /gcast 
- broadcast your message with pin in the served Chats

• /broadcast 
- broadcast your message without pin in the served chats

• /exec <code> 
- Execute any Code given by a sudo user of the bot

• /stats
- shows the Bot's system stats

• /userbotleaveall
- force the music assistant of the bot to leave all the served Chats""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅️ Back", callback_data="cbevery")
                ],
            ]
        ),
    )


# Commands for Group Admins
@Client.on_callback_query(filters.regex("cbadmins"))
async def admin_set(_, query: CallbackQuery):
    await query.answer("admins menu")
    await query.edit_message_text(
    f"""• /skip 
- skips music in the voice Chat 

• /pause 
- Pause music in the voice chat 

• /resume 
- Resumes music in the voice Chat

• /end or /stop
- stop playing music in the group's voice chat

• /cleandb
- Clears all raw files in your group which is uploaded by bot

• /userbotjoin
- invites the music assistant of the bot in your group

• /userbotleave
- Bot's music assistant will leaves your group""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅️ Back", callback_data="cbevery")
                ],
            ]
        ),
    )


# Bot about & Information
@Client.on_callback_query(filters.regex("cbabout"))
async def about_set(_, query: CallbackQuery):
    await query.edit_message_text(
    f"""‹ مرحبا بك في قسم الاعدادات  › [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})

- يمكنك الانضمام والتواصل مع المطورين عن طريق الازرار أدناه""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("‹ قناة الدعم ›", url=f"https://t.me/{SUPPORT}"),
                    InlineKeyboardButton("‹ قناة المطور ›", url=f"https://t.me/{UPDATE}")
                ],[
                    InlineKeyboardButton("‹ مطور البوت ›", url=f"https://t.me/{OWNER_USERNAME}"),
                    InlineKeyboardButton("‹ حساب المساعد ›", url=f"https://t.me/{ASSUSERNAME}")
                ],[
                    InlineKeyboardButton("‹ السورس ›", url="https://t.me/Xl444")
                ],[
                    InlineKeyboardButton("‹ رجوع ›", callback_data="cbhome")
                ],
            ]
        ),
    )


# OTHERS CALLBACK
@Client.on_callback_query(filters.regex("others"))
async def others(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""Powered By : @{UPDATE}

After you played your song some menu buttons will be comes to manage your music playing on voice chat. All the buttons are as follows :

• ⏸ 
- Resume Music
• ▶️
- Pause Music
• ⏹ 
- End Music
• ⏩
- Skip Music

Only admins can use this buttons📍""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton("Support 🚶", url=f"https://t.me/{SUPPORT}"),
                    InlineKeyboardButton("Updates 🤖", url=f"https://t.me/{UPDATE}")
                ],
            [InlineKeyboardButton("Basic Guide & Full Set-up", callback_data="setup")],
            [InlineKeyboardButton("⬅️ Back", callback_data="cbhome")]]
        ),
    )

@Client.on_callback_query(filters.regex("setup"))
async def setup(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Basic SetUp Guide for the Bot Usage :**


• Add this Bot in your Group.

• Promote it as an administrator with needed powers.

• Now send /play or /userbotjoin command to invite assistant id in your Chat.

• Your All the Set-Up is Done, Now enjoy your favourite music in your groups voice chat without any limitations.


Thanks !!
Please don't forget to Join our Group :
@{UPDATE}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅️ Back", callback_data="others")
                ],
            ]
        ),
    )
