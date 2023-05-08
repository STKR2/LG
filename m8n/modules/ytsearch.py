import logging

from search_engine_parser import GoogleSearch
from youtube_search import YoutubeSearch

import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message

from m8n import app
from m8n.utils.filters import command


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logging.getLogger("pyrogram").setLevel(logging.WARNING)


@app.on_message(command(["رابط", "اغنيه", "link"]))
async def ytsearch(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("‹ اكتب رابط واسم الاغنية للحصول على رابطها›")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("‹ يتم البحث الان ›")
        results = YoutubeSearch(query, max_results=7).to_dict()
        text = ""
        for i in range(4):
            text += f" **‹ الاسم ›** - [{results[i]['title']}](https://youtube.com{results[i]['url_suffix']})\n"
            text += f" **‹ الوصف ›** - {results[i]['duration']}\n"
            text += f" **‹ عدد المشاهدات ›** - {results[i]['views']}\n"
            text += f" **‹ قناة اليوتيوب ›** - {results[i]['channel']}\n\n"
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))
