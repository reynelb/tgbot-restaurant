from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler, CommandHandler, MessageHandler, ContextTypes, filters
)

# Etapas de la conversación
PEOPLE, DATE, TIME, NAME, PHONE, CONFIRM = range(6)

async def start_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👥 ¿Para cuántas personas es la reserva?")
    return PEOPLE

async def get_people(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["people"] = update.message.text
    await update.message.reply_text("📅 ¿Para qué fecha? (Ej: 20/07)")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("⏰ ¿A qué hora?")
    return TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["time"] = update.message.text
    await update.message.reply_text("📝 ¿Cuál es tu nombre?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📞 ¿Tu número de teléfono?")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    data = context.user_data
    resumen = (
        f"📌 *Resumen de tu reserva:*\n\n"
        f"👥 Personas: {data['people']}\n"
        f"📅 Fecha: {data['date']}\n"
        f"⏰ Hora: {data['time']}\n"
        f"📝 Nombre: {data['name']}\n"
        f"📞 Teléfono: {data['phone']}\n\n"
        "¿Confirmas la reserva? (sí / no)"
    )
    await update.message.reply_text(resumen, parse_mode="Markdown")
    return CONFIRM

async def confirm_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() in ["sí", "si", "да", "yes"]:
        # Aquí podrías guardar en DB o enviar notificación
        await update.message.reply_text("✅ ¡Reserva confirmada! Te esperamos 🎉")
    else:
        await update.message.reply_text("❌ Reserva cancelada.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Reserva cancelada.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Conversación
handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^📅 Reservar mesa$"), start_reservation)],
    states={
        PEOPLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_people)],
        DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
        TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_reservation)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
