from telegram import Update, ReplyKeyboardRemove
from telegram.ext import MessageHandler, ConversationHandler, ContextTypes, filters

FEEDBACK = range(1)
ADMIN_CHAT_ID = 123456789  # ← Reemplaza con tu ID de admin o canal

async def ask_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🗣️ ¡Tu opinión es muy importante!\n\nPor favor, escribe tu reseña sobre el servicio o la comida:",
        reply_markup=ReplyKeyboardRemove()
    )
    return FEEDBACK

async def save_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.effective_user
    name = user.full_name

    # Enviar al admin o canal
    text = f"📢 *Nueva reseña recibida:*\n\n👤 {name}\n💬 {message}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text, parse_mode="Markdown")

    await update.message.reply_text("✅ ¡Gracias por tu reseña! Nos ayuda a mejorar 🙏")
    return ConversationHandler.END

# Conversación
handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^💬 Dejar una reseña$"), ask_feedback)],
    states={
        FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_feedback)],
    },
    fallbacks=[]
)
