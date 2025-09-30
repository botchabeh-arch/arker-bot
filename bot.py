import logging
import asyncio
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import time
from zoneinfo import ZoneInfo

# 🔑 التوكن تبع البوت
TOKEN = "8303213892:AAGzX2Kxe59KUegcUMaYPtVSv54XEhB3d-c"

# 🔑 معرف القناة (خاصة)
CHANNEL_ID = -1002977291153

# إعداد اللوج
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- الأدعية ---
dua_sabah = [
    "🌅 اللهم بك أصبحنا وبك أمسينا وبك نحيا وبك نموت وإليك النشور",
    "🌅 أصبحنا وأصبح الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له"
]

dua_duhr = [
    "☀️ اللهم أعني على ذكرك وشكرك وحسن عبادتك",
    "☀️ اللهم ارزقني من حيث لا أحتسب"
]

dua_asr = [
    "🌤️ اللهم اجعل هذا اليوم مباركًا واجعلنا فيه من المقبولين",
    "🌤️ اللهم اغفر لي ولوالدي وللمؤمنين يوم يقوم الحساب"
]

dua_masaa = [
    "🌙 اللهم بك أمسينا وبك أصبحنا وبك نحيا وبك نموت وإليك المصير",
    "🌙 أمسينا وأمسى الملك لله رب العالمين، اللهم إني أسألك خير هذه الليلة"
]

# --- أوامر ---
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال وسوف يرسل الأدعية في القناة.")

async def test(update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHANNEL_ID, text="🚀 اختبار: البوت شغال و يرسل للقناة.")
    await update.message.reply_text("✅ تم إرسال رسالة اختبار في القناة.")

# --- مهمة إرسال الأدعية ---
async def send_dua(context: ContextTypes.DEFAULT_TYPE):
    job_name = context.job.name
    if job_name == "sabah":
        text = "\n".join(dua_sabah)
    elif job_name == "duhr":
        text = "\n".join(dua_duhr)
    elif job_name == "asr":
        text = "\n".join(dua_asr)
    elif job_name == "masaa":
        text = "\n".join(dua_masaa)
    else:
        text = "دعاء غير معروف"
    await context.bot.send_message(chat_id=CHANNEL_ID, text=text)

# --- التشغيل ---
async def main():
    app = Application.builder().token(TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))

    # جدولة الأدعية حسب توقيت الجزائر
    tz = ZoneInfo("Africa/Algiers")
    app.job_queue.run_daily(send_dua, time(7, 0, tzinfo=tz), name="sabah")   # الصباح
    app.job_queue.run_daily(send_dua, time(12, 30, tzinfo=tz), name="duhr")  # الظهر
    app.job_queue.run_daily(send_dua, time(15, 30, tzinfo=tz), name="asr")   # العصر
    app.job_queue.run_daily(send_dua, time(19, 0, tzinfo=tz), name="masaa")  # المساء

    print("🚀 البوت بدأ يشتغل...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
