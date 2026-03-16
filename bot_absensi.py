from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime

TOKEN = "8521724269:AAFyuMbyD91ipE-1pjela9MNFugAybx-pbU"

data = {}

def now():
    return datetime.now().strftime("%H:%M:%S")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot aktif.\nGunakan:\n/checkin\n/breaktime\n/back\n/checkout"
    )

async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    data[user] = {"checkin": now()}
    await update.message.reply_text(f"✅ {user} check-in jam {data[user]['checkin']}")

async def breaktime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"☕ {user} mulai break jam {now()}")

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"🔙 {user} selesai break jam {now()}")

async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"🛑 {user} checkout jam {now()}")

def main():
    print("Bot starting...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CommandHandler("breaktime", breaktime))
    app.add_handler(CommandHandler("back", back))
    app.add_handler(CommandHandler("checkout", checkout))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()