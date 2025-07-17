from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler, CommandHandler, MessageHandler, ContextTypes, filters
)

# Conversation steps
PEOPLE, DATE, TIME, NAME, PHONE, CONFIRM = range(6)

async def start_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👥 На сколько человек вы хотите забронировать столик?")
    return PEOPLE

async def get_people(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["people"] = update.message.text
    await update.message.reply_text("📅 На какую дату? (Напр: 20/07)")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("⏰ На какое время?")
    return TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["time"] = update.message.text
    await update.message.reply_text("📝 Как вас зовут?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📞 Ваш номер телефона?")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    data = context.user_data
    summary = (
        f"📌 *Подтверждение брони:*\n\n"
        f"👥 Количество человек: {data['people']}\n"
        f"📅 Дата: {data['date']}\n"
        f"⏰ Время: {data['time']}\n"
        f"📝 Имя: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n\n"
        "Подтверждаете бронь? (да / нет)"
    )
    await update.message.reply_text(summary, parse_mode="Markdown")
    return CONFIRM

async def confirm_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() in ["sí", "si", "да", "yes"]:
        # Here you can save to a database or send a notification
        await update.message.reply_text("✅ Бронирование подтверждено! Ждём вас 🎉")
    else:
        await update.message.reply_text("❌ Бронирование отменено.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Бронирование отменено.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Conversation handler
handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^📅 Забронировать столик$"), start_reservation)],
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
