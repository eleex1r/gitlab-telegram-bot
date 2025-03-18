from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я GitLab бот. Я буду уведомлять вас о событиях из GitLab.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Используйте /start для начала работы.')
