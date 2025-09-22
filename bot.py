import os
import yt_dlp
from telethon import TelegramClient, events

API_ID = 26430345
API_HASH = "45e8990870008b63fee8135b4a2442a1"
SESSION_NAME = "mysession"
OWNER_ID = 6582661205  

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    if not event.is_private or event.sender_id != OWNER_ID:
        return

    url = event.message.message.strip()
    if not url.startswith("http"):
        await event.reply("⚠️ ابعت لينك صحيح.")
        return

    await event.reply("⏳ جاري التحميل...")

    try:
        ydl_opts = {"format": "best", "outtmpl": "video.%(ext)s"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await event.reply("⬆️ جاري الرفع...")
        await client.send_file(event.chat_id, filename, caption="✅ تم التحميل.")

        os.remove(filename)

    except Exception as e:
        await event.reply(f"⚠️ حصل خطأ: {e}")

print("🚀 البوت شغال...")
client.start()
client.run_until_disconnected()
