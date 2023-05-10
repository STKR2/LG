from asyncio import QueueEmpty

from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream

from pyrogram import Client, filters
from pyrogram.types import Message

from m8n import app
from m8n.config import que
from m8n.database.queue import (
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from m8n.tgcalls import calls

from m8n.utils.filters import command, other_filters
from m8n.utils.decorators import sudo_users_only
from m8n.tgcalls.queues import clear, get, is_empty, put, task_done


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await app.get_chat_member(chat_id, user_id)
    except Exception:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


from m8n.utils.administrator import adminsOnly



@app.on_message(command(["تحديث", f"عيد"]) & other_filters)

async def update_admin(client, message: Message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ تم اعادة **تشغيل البوت** !\n✅ وتم **تحديث** قائمة **المشرفين.**"
    )








@app.on_message(command(["مؤقتا"]) & other_filters)
async def pause(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            " __- انت مجهول يول!__\n│\n╰ ارجع مشرف عادي وتدلل"
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(
            " __**- ماكو شي مشتغل حبيب .**__"
        )
    elif not await is_music_playing(message.chat.id):
        return await message.reply_text(
            " __**- ماكو شي مشتغل حبيب .**__"
        )
    await music_off(chat_id)
    await calls.pytgcalls.pause_stream(chat_id)
    await message.reply_text(
        f"• تم ايقاف التشغيل مؤقتا\n• By : {checking}"
    )


@app.on_message(command(["استمر"]) & other_filters)
async def resume(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            " __- انت مجهول !__\n│\n╰ ارجع ادمن وتدلل ."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(
            " __**- ماكو شي مشتغل حبيب .**__"
        )
    elif await is_music_playing(chat_id):
        return await message.reply_text(
            " __**- ماكو شي مشتغل حبيب .**__"
        )
    else:
        await music_on(chat_id)
        await calls.pytgcalls.resume_stream(chat_id)
        await message.reply_text(
            f"• تم الاستمرار بنجاح\n• By : {checking}"
        )


@app.on_message(command(["كافي"]) & other_filters)
async def stop(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            " __ - انت مجهول ماتكدر تستخدم البوت !__\n│\n╰ ارجع مشرف وتدلل"
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await calls.pytgcalls.leave_group_call(chat_id)
        await message.reply_text(
            f"• تم ايقاف التشغيل \n• بواسطة : {checking}"
        )
    else:
        return await message.reply_text(
            " __**- ماكو شي مشتغل حبيب .**__"
        )


@app.on_message(command(["سكب"]) & other_filters)
async def skip(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            " __- انت مجهول!__\n│\n╰ ارجع ادمن وتدلل ."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    chat_title = message.chat.title
    if not await is_active_chat(chat_id):
        await message.reply_text(" __**- ماكو شي مشتغل حبيب .**__")
    else:
        task_done(chat_id)
        if is_empty(chat_id):
            await remove_active_chat(chat_id)
            await message.reply_text(
                " __**- ماكو شي بقائمة الانتضار**__\n\n**•** `تم مغادرة حساب المساعد`"
            )
            await calls.pytgcalls.leave_group_call(chat_id)
            return
        else:
            await calls.pytgcalls.change_stream(
                chat_id,
                InputStream(
                    InputAudioStream(
                        get(chat_id)["file"],
                    ),
                ),
            )
            await message.reply_text(
                f"• تم تخطي الاغنية بنجاح\n• بواسطة : {checking}"
            )


@app.on_message(command(["تنظيف"]))
async def stop_cmd(_, message):
    if message.sender_chat:
        return await message.reply_text(
            " __- انت مجهول!__\n│\n╰ ارجع ادمن وتدلل ."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    chat_id = message.chat.id
    checking = message.from_user.mention
    try:
        clear(chat_id)
    except QueueEmpty:
        pass
    await remove_active_chat(chat_id)
    try:
        await calls.pytgcalls.leave_group_call(chat_id)
    except:
        pass
    await message.reply_text(
        f"✅ __تم التنظيف بنجاح **{message.chat.title}**__\n│\n╰ بواسطة {checking}"
    )
