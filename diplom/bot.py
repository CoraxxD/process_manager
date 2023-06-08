import psutil
import telegram
from telegram.ext import CommandHandler, Updater

# Insert your bot token here
bot_token = '5861413011:AAGt2WiV4H-USVXeQzo-nsaogE6TF2b1x1k'

# Initialize the Telegram bot using your API token
bot = telegram.Bot(token=bot_token)

# Define a function to get the current system status
def get_system_status():
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    return f"CPU usage: {cpu_percent}%\nRAM usage: {ram_percent}%"

# Define a function to handle the /status command
def status(update, context):
    status_message = get_system_status()
    context.bot.send_message(chat_id=update.effective_chat.id, text=status_message)

# Define a function to handle the /restart command
def restart(update, context):
    # Add code here to restart the application or service
    context.bot.send_message(chat_id=update.effective_chat.id, text="Application restarted")

# Initialize the Telegram bot updater and add command handlers
updater = Updater(bot_token)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('status', status))
dispatcher.add_handler(CommandHandler('restart', restart))

# Start the Telegram bot
updater.start_polling()
