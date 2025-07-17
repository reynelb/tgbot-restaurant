from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, ContextTypes, filters

ADMIN_PHONE = "+50760000000"  # ← Cambia por el número real del restaurante

async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📞 ¿Prefieres hablar con una persona?\n\n"
        "Puedes llamar directamente a nuestro administrador.\n"
        "¡Estaremos encantados de ayudarte! 😊"
    )

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("📲 Llamar ahora", url=f"tel:{ADMIN_PHONE}")
    ]])

    await update.message.reply_text(text, reply_markup=keyboard)

# Handler
handler = MessageHandler(filters.Regex("^📞 Contactar al administrador$"), contact_admin)
