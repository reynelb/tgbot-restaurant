from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, ContextTypes, filters, CallbackQueryHandler

# Menú simulado
MENU = {
    "Entradas": [("Bruschetta", "Pan con tomate y albahaca - $5"),
                 ("Empanadas", "Rellenas de carne - $6")],
    "Platos Principales": [("Lomo Saltado", "Con papas y arroz - $12"),
                           ("Paella", "Con mariscos - $15")],
    "Bebidas": [("Jugo Natural", "De naranja o piña - $3"),
                ("Vino Tinto", "Copa de la casa - $6")]
}


def build_category_keyboard():
    keyboard = [
        [InlineKeyboardButton(category, callback_data=f"menu_{category}")]
        for category in MENU.keys()
    ]
    return InlineKeyboardMarkup(keyboard)


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "📋 Estas son las categorías del menú:",
            reply_markup=build_category_keyboard()
        )


async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.replace("menu_", "")
    items = MENU.get(category, [])
    if not items:
        await query.edit_message_text("❌ No se encontraron elementos.")
        return

    text = f"📂 *{category}*\n\n"
    for name, description in items:
        text += f"• *{name}*: {description}\n"
    await query.edit_message_text(text, parse_mode="Markdown")


# Handlers
handler = MessageHandler(filters.Regex("^🍽 Ver menú$"), show_menu)
callback_handler = CallbackQueryHandler(handle_menu_selection, pattern="^menu_")
