import logging
from telegram.ext import Application
from datetime import time
import pytz

# ========= إعدادات =========
import os
TOKEN = os.getenv("8303213892:AAFxBUaTaWylw4yEydvRT7ruh6BPT_t4IHA")  # ناخذ التوكن من المتغيرات البيئية
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1002977291153"))

ADHKAR_MORNING = ["أصبحنا وأصبح الملك لله...", "اللهم بك أصبحنا..."]
ADHKAR_EVENING = ["أمسينا وأمسى الملك لله...", "اللهم بك أمسينا..."]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def morning_job(context):
    await context.bot.send_message(chat_id=CHANNEL_ID, text="🕊️ أذكار الصباح:\n\n" + "\n\n".join(ADHKAR_MORNING))

async def evening_job(context):
    await context.bot.send_message(chat_id=CHANNEL_ID, text="🌙 أذكار المساء:\n\n" + "\n\n".join(ADHKAR_EVENING))

def main():
    application = Application.builder().token(TOKEN).build()
    job_queue = application.job_queue

    tz = pytz.timezone("Africa/Algiers")

    job_queue.run_daily(morning_job, time=time(7, 0, tzinfo=tz))
    job_queue.run_daily(evening_job, time=time(18, 0, tzinfo=tz))

    print("✅ البوت يعمل...")
    application.run_polling()

if __name__ == "__main__":
    main()