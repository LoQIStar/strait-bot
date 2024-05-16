from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Set your Telegram bot token and Claude 3 API key
TELEGRAM_BOT_TOKEN = '7023844989:AAFtCtdgvaEHNy5kq7lSlioBFaNUhlGWvVQ'
CLAUDE_API_KEY = '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'

# Define the start command handler
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        rf'Hi {user.mention_html()}!',
        reply_markup=ForceReply(selective=True),
    )

# Define the help command handler
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')

# Define the message handler
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    # Send the user's message to Claude 3 API
    response = requests.post(
        'https://api.anthropic.com/v1/claude-3',
        headers={
            'Authorization': f'Bearer {CLAUDE_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            'prompt': user_message,
            'max_tokens': 150
        }
    )

    # Get the response text
    response_text = response.json().get('completion', '').strip()

    # Send the response back to the user
    update.message.reply_text(response_text)

# Main function to run the bot
def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(TELEGRAM_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
