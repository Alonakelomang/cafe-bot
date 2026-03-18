from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import pytz

TOKEN = "8521724269:AAFyuMbyD91ipE-1pjela9MNFugAybx-pbU"

data = {}

# timezone Indonesia
tz = pytz.timezone("Asia/Jakarta")


def now():
    return datetime.now(tz)


def format_duration(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours > 0:
        return f"{hours} jam {minutes} menit"
    else:
        return f"{minutes} menit"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot aktif.\nGunakan:\n/checkin\n/break atau /rest\n/back\n/checkout"
    )


async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    checkin_time = now()
    end_time = checkin_time + timedelta(hours=8)

    data[user] = {
        "checkin": checkin_time,
        "break_start": None,
        "total_break": timedelta()
    }

    await update.message.reply_text(
        f"✅ {user} check-in jam {checkin_time.strftime('%H:%M:%S')}\n"
        f"🕒 Jam kerja: {checkin_time.strftime('%H:%M:%S')} - {end_time.strftime('%H:%M:%S')}"
    )


async def break_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    if user not in data or "checkin" not in data[user]:
        await update.message.reply_text("❌ Kamu belum check-in")
        return

    if data[user]["break_start"] is not None:
        await update.message.reply_text("⚠️ Kamu sudah dalam status break")
        return

    data[user]["break_start"] = now()

    await update.message.reply_text(
        f"☕ {user} mulai break jam {data[user]['break_start'].strftime('%H:%M:%S')}"
    )


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    if user not in data or data[user].get("break_start") is None:
        await update.message.reply_text("❌ Kamu belum mulai break")
        return

    break_end = now()
    break_start = data[user]["break_start"]

    duration = break_end - break_start
    data[user]["total_break"] += duration
    data[user]["break_start"] = None

    msg = (
        f"🔙 {user} selesai break jam {break_end.strftime('%H:%M:%S')}\n"
        f"⏱ Durasi break: {format_duration(duration)}"
    )

    # cek kelebihan break
    if duration > timedelta(hours=1):
        excess = duration - timedelta(hours=1)
        msg += f"\n⚠️ Kelebihan break: {format_duration(excess)}"

    await update.message.reply_text(msg)


async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    if user not in data or "checkin" not in data[user]:
        await update.message.reply_text("❌ Kamu belum check-in")
        return

    checkout_time = now()
    checkin_time = data[user]["checkin"]
    total_break = data[user]["total_break"]

    work_duration = checkout_time - checkin_time - total_break

    msg = (
        f"🛑 {user} checkout jam {checkout_time.strftime('%H:%M:%S')}\n"
        f"⏱ Total kerja: {format_duration(work_duration)}"
    )

    # cek lembur
    if work_duration > timedelta(hours=8):
        overtime = work_duration - timedelta(hours=8)
        msg += f"\n🔥 Lembur: {format_duration(overtime)}"

    await update.message.reply_text(msg)

    # reset data user
    del data[user]


def main():
    print("Bot starting...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("checkin", checkin))

    app.add_handler(CommandHandler("break", break_time))
    app.add_handler(CommandHandler("rest", break_time))

    app.add_handler(CommandHandler("back", back))
    app.add_handler(CommandHandler("checkout", checkout))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()