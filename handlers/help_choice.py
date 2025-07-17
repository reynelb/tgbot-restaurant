from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, ContextTypes, filters

# Estados de la conversación
PREFERENCE, ALLERGY = range(2)

# Base de datos simulada de platos con etiquetas
MENU_TAGS = {
    "Lomo Saltado": ["carne"],
    "Paella": ["mariscos"],
    "Ensalada César": ["ligero", "vegetariano"],
    "Curry Vegano": ["vegetariano", "picante"],
    "Bruschetta": ["ligero", "vegetariano"]
}

async def start_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_kb = [["Carne", "Vegetariano"], ["Ligero", "Picante"], ["Me da igual"]]
    await update.message.reply_text(
        "🍴 ¿Qué tipo de comida prefieres hoy?",
        reply_markup=ReplyKeyboardMarkup(reply_kb, resize_keyboard=True)
    )
    return PREFERENCE

async def get_preference(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pref = update.message.text.lower()
    context.user_data["preference"] = pref
    await update.message.reply_text(
        "⚠ ¿Tienes alguna alergia o ingrediente que evitar?",
        reply_markup=ReplyKeyboardRemove()
    )
    return ALLERGY

async def get_allergy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    allergy = update.message.text.lower()
    pref = context.user_data["preference"]

    # Filtrar menú según preferencia
    suggestions = []
    for dish, tags in MENU_TAGS.items():
        if pref == "me da igual" or pref in tags:
            if allergy not in dish.lower():
                suggestions.append(dish)

    if suggestions:
        text = "👨‍🍳 Según tus preferencias, te sugerimos:\n\n"
        text += "\n".join(f"• {s}" for s in suggestions[:3])
    else:
        text = "😕 No encontramos opciones que coincidan exactamente, pero puedes revisar el menú completo."

    await update.message.reply_text(text)
    return ConversationHandler.END

# Cancelar
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Asistente cancelado.")
    return ConversationHandler.END

# Conversación
handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^🧭 Ayuda para elegir$"), start_help)],
    states={
        PREFERENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_preference)],
        ALLERGY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_allergy)],
    },
    fallbacks=[],
)
