from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, ContextTypes, filters

ADMIN_PHONE = "0000000"  # ← Замените на настоящий номер ресторана

async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📞 Предпочитаете поговорить с человеком?\n\n"
        "Вы можете напрямую позвонить нашему администратору.\n"
        "Мы будем рады помочь вам! 😊"
    )

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("📲 Позвонить сейчас", url=f"tel:{ADMIN_PHONE}")
    ]])

    await update.message.reply_text(text, reply_markup=keyboard)

# Handler
handler = MessageHandler(filters.Regex("^📞 Связаться с администратором$"), contact_admin)
