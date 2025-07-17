from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, MessageHandler, ContextTypes, filters

# Simulamos menú como antes
MENU = {
    "Entradas": [("Bruschetta", "$5"), ("Empanadas", "$6")],
    "Platos Principales": [("Lomo Saltado", "$12"), ("Paella", "$15")],
    "Bebidas": [("Jugo", "$3"), ("Vino", "$6")]
}

# Creamos botón por categoría
def build_category_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(cat, callback_data=f"preorder_{cat}")]
        for cat in MENU
    ] + [[InlineKeyboardButton("✅ Confirmar pedido", callback_data="preorder_confirm")]])

# Inicio del preorder
async def start_preorder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["preorder"] = []
    await update.message.reply_text(
        "📝 Elige los platos que quieres que estén listos a tu llegada:",
        reply_markup=build_category_keyboard()
    )

# Mostrar platos dentro de una categoría
async def select_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.replace("preorder_", "")
    if category == "confirm":
        return await confirm_preorder(update, context)

    items = MENU.get(category, [])
    keyboard = [
        [InlineKeyboardButton(f"{name} – {price}", callback_data=f"add_{name}")]
        for name, price in items
    ]
    keyboard.append([InlineKeyboardButton("⬅ Volver", callback_data="preorder_back")])

    await query.edit_message_text(
        f"🍽 *{category}* - Elige uno o más platos:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Agregar plato
async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    item = query.data.replace("add_", "")
    context.user_data.setdefault("preorder", []).append(item)
    await query.edit_message_text(f"✅ Agregado: *{item}*", parse_mode="Markdown")
    await query.message.reply_text(
        "👉 Puedes seguir eligiendo platos:",
        reply_markup=build_category_keyboard()
    )

# Confirmar pedido
async def confirm_preorder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    items = context.user_data.get("preorder", [])
    if not items:
        await query.edit_message_text("⚠ No has seleccionado nada aún.")
        return

    summary = "\n".join(f"• {i}" for i in items)
    await query.edit_message_text(
        f"📦 *Pedido confirmado:*\n\n{summary}\n\n¡Lo tendremos listo a tu llegada!",
        parse_mode="Markdown"
    )


# Handlers
handler = MessageHandler(filters.Regex("^⏱ Pedir comida con anticipación$"), start_preorder)
callback_category = CallbackQueryHandler(select_category, pattern="^preorder_")
callback_add = CallbackQueryHandler(add_item, pattern="^add_")
