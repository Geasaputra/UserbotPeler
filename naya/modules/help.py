# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT


import asyncio
import datetime
import re
import sys
from datetime import datetime
from os import environ, getpid, execle

import dotenv
import heroku3
import psutil
import urllib3

HAPP = None
import urllib3 
from time import time
from naya.utils.db import *
from naya.utils.db.accesdb import *
from naya.utils.db.accesdb import get_expired_date
from pyrogram.raw.functions import Ping
from pyrogram.types import *

from naya.config import *

from . import *
from .ping import START_TIME, _human_time_duration
from .system import anu_heroku 

from . import (
    StartTime,
    time_formatter,)
    

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

photo = "naya/resources/logo.jpg"

@app.on_callback_query(
    filters.regex("sys_stats")
)
async def _sys_callback(
    client,
    cq: CallbackQuery,
):
    text = sys_stats()
    await app.answer_callback_query(
        cq.id,
        text,
        show_alert=True,
    )

def sys_stats():
    cpu = psutil.cpu_percent()
    mem = (
        psutil.virtual_memory().percent
    )
    disk = psutil.disk_usage(
        "/"
    ).percent
    process = psutil.Process(getpid())
    stats = f"""
PYROBOT-Premium
-----------------------
UPTIME: {time_formatter((time.time() - StartTime) * 1000)}
BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
CPU: {cpu}%
RAM: {mem}%
DISK: {disk}%
-----------------------

Copyright (C) 2023-present fvnky
"""
    return stats

@bots.on_message(filters.command(["help", "alive"], cmd) & filters.me)
async def _(client, message):
    if message.command[0] == "alive":
        text = f"user_alive_command {message.id} {message.from_user.id}"
    if message.command[0] == "help":
        text = "user_help_command"
    try:
        x = await client.get_inline_bot_results(app.me.username, text)
        for m in x.results:
            await message.reply_inline_bot_result(x.query_id, m.id)
    except Exception as error:
        await message.reply(error)
    return await message.delete()
    
@app.on_inline_query(filters.regex("^user_alive_command"))
async def _(client, inline_query):
    inline_query.query.split()    
    status1 = "premium"
    for bot in botlist:
        users = 0
        group = 0
        async for dialog in bot.get_dialogs():
            if dialog.chat.type == enums.ChatType.PRIVATE:
                users += 1
            elif dialog.chat.type in (
                enums.ChatType.GROUP,
                enums.ChatType.SUPERGROUP,
            ):
                group += 1
        if bot.me.id in DEVS:
            status = "founder"
        elif bot.me.id == OWNER:
            status = "owner"        
        else:
            status = "admin"
        start = datetime.now()
        await bot.invoke(Ping(ping_id=0))
        ping = (datetime.now() - start).microseconds / 1000
        uptime_sec = (datetime.utcnow() - START_TIME).total_seconds()
        uptime = await _human_time_duration(int(uptime_sec))
	remaining_days = await get_expired_date(ex.id)
        msg = f"""
<b>Pyro-bot</b>
     <b>status:</b> <code>{status1}[{status}]</code>
          <b>dc_id:</b> <code>{bot.me.dc_id}
          <b>ping_dc:</b> <code>{ping} ms</code>
          <b>peer_users:</b> <code>{users} users</code>
          <b>peer_group:</b> <code>{group} group</code>
          <b>uptime:</b> <code>{uptime}</code>
          <b>expired:</b> <code>{remaining_days}</code>
"""
        await client.answer_inline_query(
            inline_query.id,
            cache_time=300,
            results=[
                InlineQueryResultArticle(
                    title="💬",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="ᴄʟᴏsᴇ", callback_data="alv_cls"    
                                ),
                                InlineKeyboardButton(
                                    text="sᴛᴀᴛs", callback_data="sys_stats"
                                 
                                ),
                            ]
                        ]
                    ),
                    input_message_content=InputTextMessageContent(msg),
                )
            ],
        )


@app.on_inline_query(filters.regex("^user_help_command"))
async def _(client, inline_query):
    msg = f"""
    <b>Help Modules<b>
     <b>Prefixes:</b> <code>{cmd}</code></b>
     <b>Commands: {len(CMD_HELP)}</b>
    """
    await client.answer_inline_query(
        inline_query.id,
        cache_time=300,
        results=[
            (
                InlineQueryResultArticle(
                    title="Help Module",
                    reply_markup=InlineKeyboardMarkup(
                        paginate_modules(0, CMD_HELP, "help")
                    ),
                    input_message_content=InputTextMessageContent(msg),
                )
            )
        ],
    )


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def _(client, callback_query):
    mod_match = re.match(r"help_module\((.+?)\)", callback_query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", callback_query.data)
    next_match = re.match(r"help_next\((.+?)\)", callback_query.data)
    back_match = re.match(r"help_back", callback_query.data)
    if mod_match:
        module = mod_match[1].replace(" ", "_")
        text = f"<b>{CMD_HELP[module].__HELP__}</b>\n"
        button = [[InlineKeyboardButton("• ᴋᴇᴍʙᴀʟɪ •", callback_data="help_back")]]
        await callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True,
        )
    prev_text = f"""
    <b>Help Modules<b>
     <b>Prefixes:</b> <code>{cmd}</code></b>
     <b>Commands: {len(CMD_HELP)}</b>
    """
    if prev_match:
        curr_page = int(prev_match[1])
        await callback_query.edit_message_text(
            text=prev_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, CMD_HELP, "help")
            ),
            disable_web_page_preview=True,
        )
    next_text = f"""
    <b>Help Modules<b>
     <b>Prefixes:</b> <code>{cmd}</code></b>
     <b>Commands: {len(CMD_HELP)}</b>
    """
    if next_match:
        next_page = int(next_match[1])
        await callback_query.edit_message_text(
            text=next_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, CMD_HELP, "help")
            ),
            disable_web_page_preview=True,
        )
    back_text = f"""
    <b>Help Module<b>
     <b>Prefixes:</b> <code>{cmd}</code></b>
     <b>Commands: {len(CMD_HELP)}</b>
    """
    if back_match:
        await callback_query.edit_message_text(
            text=back_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(0, CMD_HELP, "help")),
            disable_web_page_preview=True,
        )

@app.on_message(filters.command(["ubotcheck"]) & filters.private)
async def check_active(client, message):
    if message.from_user.id not in ADMINS:
        await message.reply("You are not registered in the Admin list.")
        return
    try:
        user_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.reply("use format: /ubotcheck user_id")
        return

    expired_date = await get_expired_date(user_id)
    if expired_date is None:
        await message.reply(f"User {user_id} not yet activated.")
    else:
        await message.reply(f"User {user_id} Until Date {expired_date}.")


@app.on_message(filters.command(["prem"]) & filters.private)
async def handle_grant_access(client: Client, message: Message):
    text = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.reply_text("I can't find that user.")
            return
        username = text[1]
        try:
            user = await client.get_users(username)
        except ValueError:
            user = None
        if user is None:
            await message.reply_text(f"I can't find that user {username} .")
            return
        user_id = user.id

    if message.from_user.id not in DEVS:
        await message.reply_text("only admins can grant access.")
        return

    duration = 1
    if text is not None and len(text) >= 3:
        try:
            duration = int(text[2])
        except ValueError:
            await message.reply_text("No month_number provided.")
            return

    await check_and_grant_user_access(user_id, duration)
    await message.reply_text(f"Done! {user_id} for {duration} month.")

	
@app.on_message(filters.command(["unprem"]) & filters.private)
async def handle_revoke_access(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.reply_text("I can't find that user.")
            return
        username = text[1]
        try:
            user = await client.get_users(username)
        except ValueError:
            user = None
        if user is None:
            await message.reply_text(f"I can't find that user {username} .")
            return
        user_id = user.id

    if message.from_user.id not in DEVS:
        await message.reply_text("Maaf, hanya admin yang dapat mencabut akses.")
        return

    await delete_user_access(user_id)
    await message.reply_text(f"Akses dicabut untuk pengguna {user_id}.")

    await check_and_grant_user_access(user_id, duration)
    await message.reply_text(f"Done! {user_id} for {duration} month.")
    
@app.on_message(filters.command(["user"]) & filters.private)
async def usereee(_, message):
    user_id = message.from_user.id
    if user_id not in (OWNER, DEVS):
        return await message.reply(
            "❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya OWNER yang bisa menggunakan perintah ini"
        )
    count = 0
    user = ""
    for X in botlist:
        try:
            count += 1
            user += f"""
❏ USERBOT KE {count}
 ├ AKUN: <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
 ╰ ID: <code>{X.me.id}</code>
"""
        except BaseException:
            pass
    if len(str(user)) > 4096:
        with BytesIO(str.encode(str(user))) as out_file:
            out_file.name = "userbot.txt"
            await message.reply_document(
                document=out_file,
            )
    else:
        await message.reply(f"<b>{user}</b>")


@app.on_callback_query(filters.regex("^alv_cls"))
async def _(cln, cq): 
    cq.data.split()
    unPacked = unpackInlineMessage(cq.inline_message_id)
    for bot in botlist:
        if cq.from_user.id == int(bot.me.id):
            await bot.delete_messages(
                chat_id=unPacked.chat_id,
                message_ids=[unPacked.message_id]
            )
            


@app.on_callback_query(filters.regex("cl_ad"))
async def _(_, query: CallbackQuery):
    await query.message.delete()


@app.on_callback_query(filters.regex("multi"))
async def _(_, query: CallbackQuery):
    return await query.edit_message_text(
        "<b>Disini kamu bisa menambahkan, menghapus serta melihat variabel dan value, seperti OPENAI_API, SESSION2-SESSION10.</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Tambah Variabel", callback_data="sesi"),
                    InlineKeyboardButton(text="Hapus Variabel", callback_data="hapus"),
                ],
                [
                    InlineKeyboardButton(text="Cek Variabel", callback_data="get"),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="setong"),
                ],
                [
                    InlineKeyboardButton(text="Tutup", callback_data="cl_ad"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex("pm"))
async def _(_, query: CallbackQuery):
    await query.message.delete()
    await query.message.reply_photo(
        photo=photo,
        caption="<b> ☺️ Fitur ini akan hadir dalam beberapa pekan\n\nTunggu update nya di @KynanSupport.</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Kembali", callback_data="setong"),
                ],
                [
                    InlineKeyboardButton(text="Tutup", callback_data="cl_ad"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex("log"))
async def _(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.message.delete()
    try:
        log = await app.ask(
            user_id,
            "<b>Silakan masukkan botlog grup id anda.\nContoh : -100XXXXXX\n\nKetik /cancel untuk membatalkan proses.</b>",
            timeout=120,
        )
    except asyncio.TimeoutError:
        return await app.send_message(user_id, "Waktu Telah Habis")

    if await batal(query, log.text):
        return

    botlog = log.text
    await set_botlog(user_id, botlog)
    buttons = [
        [
            InlineKeyboardButton(text="Kembali", callback_data="multi"),
            InlineKeyboardButton("Tutup", callback_data="cl_ad"),
        ],
    ]
    await app.send_message(
        user_id,
        f"**Berhasil mengatur botlog grup anda menjadi `{botlog}`.**",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("inpo"))
async def _(_, query):
    await query.message.delete()
    await query.message.reply_photo(
        photo=photo,
        caption="<b> Halo guys barang kali lu butuh nokos luar id 1,7,3,5,6 datang ae ke  @balokmenes.</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [   
                    InlineKeyboardButton(text="ᴏᴡɴᴇʀ", user_id=OWNER),
                    InlineKeyboardButton(text="ᴛᴜᴛᴜᴘ", callback_data="cl_ad"),
                ]
            ]
        ),
    )


@app.on_callback_query(filters.regex("setong"))
async def _(_, query: CallbackQuery):
    return await query.edit_message_text(
        f"""
    <b> ☺️Halo aku adalah <a href=tg://openmessage?user_id={query.message.from_user.id}>{query.message.from_user.first_name} {query.message.from_user.last_name or ''}</a> asisten mu yang siap membantu kamu ! \n Apa yang kamu butuhkan ?.</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Multi Client", callback_data="multi"),
                    InlineKeyboardButton(text="Restart", callback_data="retor"),
                ],
                [
                    InlineKeyboardButton(text="Logger", callback_data="log"),
                    InlineKeyboardButton(text="PM Permit", callback_data="pm"),
                ],
                [
                    InlineKeyboardButton(text="Tutup", callback_data="cl_ad"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex("restart"))
async def _(_, query: CallbackQuery):
    try:
        await query.edit_message_text("<b>Processing...</b>")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await asyncio.sleep(2)
    await query.edit_message_text(f"✅ <b>{app.me.mention} Berhasil Di Restart.</b>")
    args = [sys.executable, "-m", "naya"]
    execle(sys.executable, *args, environ)


@app.on_callback_query(filters.regex("retor"))
async def _(_, query: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(text="✅ Restart", callback_data="restart"),
            InlineKeyboardButton("❌ Tidak", callback_data="cl_ad"),
        ],
    ]
    await query.edit_message_text(
        "<b>Apakah kamu yakin ingin Melakukan Restart ?</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
    )




@app.on_message(filters.command(["getotp", "getnum"]) & filters.private)
async def _(_, message):
    user_id = message.from_user.id
    if len(message.command) < 2:
        return await app.send_message(
            message.chat.id,
            f"<code>{message.text} user_id userbot yang aktif</code>",
            reply_to_message_id=message.id,
        )
    elif user_id not in (OWNER, DEVS):
        return await message.reply(
            "❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya OWNER yang bisa menggunakan perintah ini"
        )
    try:
        for X in botlist:
            if int(message.command[1]) == X.me.id:
                if message.command[0] == "getotp":
                    async for otp in X.search_messages(777000, limit=1):
                        if otp.text:
                            return await app.send_message(
                                message.chat.id,
                                otp.text,
                                reply_to_message_id=message.id,
                            )
                        else:
                            return await app.send_message(
                                message.chat.id,
                                "<code>Kode Otp Tidak Di Temukan</code>",
                                reply_to_message_id=message.id,
                            )
                elif message.command[0] == "getnum":
                    return await app.send_message(
                        message.chat.id,
                        X.me.phone_number,
                        reply_to_message_id=message.id,
                    )
    except Exception as error:
        return await app.send_message(
            message.chat.id, error, reply_to_message_id=message.id
        )


@app.on_callback_query(filters.regex("sesi"))
async def _(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.message.delete()
    try:
        var = await app.ask(
            user_id,
            "<b>Silakan masukkan variabel.\nContoh : SESSION2\n\nKetik /cancel untuk membatalkan proses.</b>",
            timeout=120,
        )
    except asyncio.TimeoutError:
        return await app.send_message(user_id, "Waktu Telah Habis")

    if await batal(query, var.text):
        return

    variable = var.text

    try:
        val = await app.ask(
            user_id,
            "<b>Silakan masukkan value.\nContoh : 02ODJDOEMXNXXXXX\n\nKetik /cancel untuk membatalkan proses.</b>",
            timeout=120,
        )
    except asyncio.TimeoutError:
        return await app.send_message(user_id, "Waktu Telah Habis")

    if await batal(query, val.text):
        return

    value = val.text
    if "HEROKU_APP_NAME" in os.environ and "HEROKU_API_KEY" in os.environ:
        api_key = os.environ["HEROKU_API_KEY"]
        app_name = os.environ["HEROKU_APP_NAME"]
        heroku = heroku3.from_key(api_key)
        hero = heroku.apps()[app_name]
        config_vars = hero.config()
        config_vars[variable] = value
        buttons = [
            [
                InlineKeyboardButton(text="Kembali", callback_data="multi"),
                InlineKeyboardButton("Tutup", callback_data="cl_ad"),
            ],
        ]
        await app.send_message(
            user_id,
            f"**Berhasil mengatur variable `{variable}` dengan value `{value}`\n\nJangan lupa untuk melakukan restart setelah menambah variabel baru.**",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        # herotod.update_config(config_vars)
    else:
        path = ".env"
        with open(path, "a") as file:
            file.write(f"\n{variable}={value}")
        if dotenv.get_key(path, variable):
            buttons = [
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            await app.send_message(
                user_id,
                f"**Berhasil mengatur variable `{variable}` dengan value `{value}`\n\nJangan lupa untuk melakukan restart setelah menambah variabel baru.**",
                reply_markup=InlineKeyboardMarkup(buttons),
            )


async def batal(query, text):
    if text.startswith("/cancel"):
        user_id = query.from_user.id
        await app.send_message(user_id, "<b>Dibatalkan !</b>")
        return True
    return False


@app.on_callback_query(filters.regex("hapus"))
async def _(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.message.delete()
    try:
        ver = await app.ask(
            user_id,
            "<b>Silakan masukkan variabel.\nContoh : SESSION2\n\nKetik /cancel untuk membatalkan proses.</b>",
            timeout=120,
        )
    except asyncio.TimeoutError:
        return await app.send_message(user_id, "Waktu Telah Habis")

    if await batal(query, ver.text):
        return

    pariabel = ver.text
    if "HEROKU_APP_NAME" in os.environ and "HEROKU_API_KEY" in os.environ:
        api_key = os.environ["HEROKU_API_KEY"]
        app_name = os.environ["HEROKU_APP_NAME"]
        heroku = heroku3.from_key(api_key)
        hero = heroku.apps()[app_name]
        config_vars = hero.config()
        del config_vars[pariabel]
        buttons = [
            [
                InlineKeyboardButton(text="Kembali", callback_data="multi"),
                InlineKeyboardButton("Tutup", callback_data="cl_ad"),
            ],
        ]
        await app.send_message(
            user_id,
            f"**Berhasil menghapus variable `{pariabel}`\n\nJangan lupa untuk melakukan restart setelah menghapus variabel.**",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        path = ".env"
        dotenv.unset_key(path, pariabel)

        if dotenv.get_key(path, pariabel) is None:
            buttons = [
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            await app.send_message(
                user_id,
                f"**Berhasil menghapus variable `{pariabel}`\n\nJangan lupa untuk melakukan restart setelah menghapus variabel.**",
                reply_markup=InlineKeyboardMarkup(buttons),
            )


@app.on_callback_query(filters.regex("get"))
async def _(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.message.delete()
    try:
        get = await app.ask(
            user_id,
            "<b>Silakan masukkan variabel.\nContoh : SESSION2\n\nKetik /cancel untuk membatalkan proses.</b>",
            timeout=120,
        )
    except asyncio.TimeoutError:
        return await app.send_message(user_id, "Waktu Telah Habis")

    if await batal(query, get.text):
        return

    variable = get.text
    if anu_heroku():
        if variable in os.environ:
            buttons = [
                [
                    InlineKeyboardButton(text="Tambah Variabel", callback_data="sesi"),
                    InlineKeyboardButton(
                        text="Hapus Variabel", callback_data="remsesi"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            return await app.send_message(
                user_id,
                f"<b>{variable}:</b> <code>{os.environ[variable]}</code>",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            buttons = [
                [
                    InlineKeyboardButton(text="Tambah Variabel", callback_data="sesi"),
                    InlineKeyboardButton(
                        text="Hapus Variabel", callback_data="remsesi"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            return await app.send_message(
                user_id,
                f"<b>Tidak ada <code>{variable}</code> ditemukan.</b>",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
    else:
        path = ".env"
        if output := dotenv.get_key(path, variable):
            buttons = [
                [
                    InlineKeyboardButton(text="Tambah Variabel", callback_data="sesi"),
                    InlineKeyboardButton(
                        text="Hapus Variabel", callback_data="remsesi"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            await app.send_message(
                user_id,
                f"<b>{variable}:</b> <code>{os.environ[variable]}</code>",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            buttons = [
                [
                    InlineKeyboardButton(text="Tambah Variabel", callback_data="sesi"),
                    InlineKeyboardButton(
                        text="Hapus Variabel", callback_data="remsesi"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            return await app.send_message(
                user_id,
                f"<b>Tidak ada <code>{variable}</code> ditemukan.</b>",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
