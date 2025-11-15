import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import FSInputFile

BOT_TOKEN = "8395895550:AAE8ucM2C_YZ76vAxcA7zInt1Nv41Fcm6NQ"
OWNER_ID = 8395895550

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DATA_FILE = "data.json"

# JSON INIT
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"media": [], "users": []}, f, indent=4)


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ─────────────────────────────────────────────
# START HANDLER — ONLY WELCOME PHOTOS + TEXT
# ─────────────────────────────────────────────
@dp.message(Command("start"))
async def start(msg: types.Message):

    data = load_data()

    # SAVE USER
    if msg.from_user.id not in data["users"]:
        data["users"].append(msg.from_user.id)
        save_data(data)

    # MULTIPLE WELCOME PHOTOS FOLDER
    folder = "ss"

    if os.path.exists(folder):
        files = sorted(os.listdir(folder))

        for index, file in enumerate(files):
            path = f"{folder}/{file}"

            if not file.lower().endswith(("jpg", "jpeg", "png")):
                continue

            if index == 0:
                caption = (
                    "▶️➡️ [𝘾𝙇𝙄𝘾𝙆 𝙃𝙀𝙍𝙀 𝙏𝙊 𝙒𝘼𝙏𝘾𝙃 𝘿𝙀𝙈𝙊 𝙋𝙍𝙊𝙊𝙁](https://t.me/Shelbypreviewbot?start=BQADAQADKw0AAkOGaESa3PDa4Iv_JRYE)\n\n"
                    "😬 INTERESTED TO BUY VIDEOS ❓❓\n\n"
                    "𝗔𝗻𝘆 𝗜𝘀𝘀𝘂𝗲? 𝗗𝗼𝘂𝗯𝘁? 𝗙𝗲𝗲𝗹 𝗙𝗿𝗲𝗲 𝗧𝗼 𝗔𝘀𝗸 😬\n"
                    "𝗛𝘆 𝗯𝗿𝗼𝗼 𝗪𝗮𝗻𝗻𝗮 𝗕𝘂𝘆 𝗩𝗶𝗱𝗲𝗼𝘀 ???"
                )

                await msg.answer_photo(
                    FSInputFile(path),
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await msg.answer_photo(FSInputFile(path))

    # DO NOT SEND ADDED MEDIA HERE
    return


# ─────────────────────────────────────────────
# ADD (ADMIN ONLY)
# ─────────────────────────────────────────────
@dp.message(Command("add"))
async def add_cmd(msg: types.Message):
    if msg.from_user.id != OWNER_ID:
        return await msg.reply("❌ Only Admin Allowed")

    await msg.reply("📥 Send photo/video/text to ADD.")


@dp.message()
async def save_media(msg: types.Message):

    if msg.from_user.id != OWNER_ID:
        return

    data = load_data()

    # PHOTO
    if msg.photo:
        f = msg.photo[-1]
        path = f"media/photo_{f.file_id}.jpg"
        await bot.download(f, path)

        caption = msg.caption if msg.caption else None

        data["media"].append({
            "type": "photo",
            "file": path,
            "caption": caption
        })
        save_data(data)
        return await msg.reply("📸 Photo Added!")

    # VIDEO
    if msg.video:
        f = msg.video
        path = f"media/video_{f.file_id}.mp4"
        await bot.download(f, path)

        caption = msg.caption if msg.caption else None

        data["media"].append({
            "type": "video",
            "file": path,
            "caption": caption
        })
        save_data(data)
        return await msg.reply("🎥 Video Added!")

    # TEXT
    if msg.text and not msg.text.startswith("/"):
        data["media"].append({
            "type": "text",
            "text": msg.text
        })
        save_data(data)
        return await msg.reply("📝 Text Added!")


# ─────────────────────────────────────────────
# DEMO — SEND ALL ADDED MEDIA
# ─────────────────────────────────────────────
@dp.message(Command("demo"))
async def demo(msg: types.Message):

    data = load_data()

    for m in data["media"]:

        if m["type"] == "text":
            await msg.answer(m["text"])

        elif m["type"] == "photo":
            await msg.answer_photo(
                FSInputFile(m["file"]),
                caption=m["caption"] if m["caption"] else None
            )

        elif m["type"] == "video":
            await msg.answer_video(
                FSInputFile(m["file"]),
                caption=m["caption"] if m["caption"] else None
            )


# ─────────────────────────────────────────────
# BROADCAST — ADMIN
# ─────────────────────────────────────────────
@dp.message(Command("broadcast"))
async def broadcast(msg: types.Message):

    if msg.from_user.id != OWNER_ID:
        return await msg.reply("❌ Only Admin Allowed")

    text = msg.text.replace("/broadcast", "").strip()
    if not text:
        return await msg.reply("Use: `/broadcast your msg`")

    data = load_data()
    users = data["users"]

    sent = 0
    for uid in users:
        try:
            await bot.send_message(uid, text)
            sent += 1
        except:
            pass

    await msg.reply(f"📢 Sent to {sent} users!")


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
