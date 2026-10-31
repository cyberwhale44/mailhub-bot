import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("📧 Create Email", callback_data="create")],
        [InlineKeyboardButton("📥 My Inbox", callback_data="inbox")],
        [InlineKeyboardButton("📤 Send Email", callback_data="send")],
        [InlineKeyboardButton("👤 My Account", callback_data="account")],
    ]

    await update.message.reply_text(
        "Welcome to MailHub! 📧\n\n"
        "Your personal email management assistant.\n\n"
        "Choose an option below:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context):
    query = update.callback_query
    await query.answer()

    messages = {
        "create": "📧 Email registration will be available soon.",
        "inbox": "📥 Your inbox will appear here.",
        "send": "📤 Email sending will be available soon.",
        "account": "👤 Your account information will appear here."
    }

    await query.message.reply_text(messages.get(query.data, "Unknown option."))

async def help_command(update: Update, context):
    await update.message.reply_text(
        "/start - Open MailHub\n"
        "/help - Show available commands"
    )

def main():
    if not TOKEN:
        raise RuntimeError("Telegram bot token is missing.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(buttons))

    print("MailHub is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
