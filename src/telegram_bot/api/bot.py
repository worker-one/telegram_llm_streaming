import logging
import logging.config
import os

import telebot
from dotenv import find_dotenv, load_dotenv
from langchain_fireworks import ChatFireworks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv(usecwd=True))  # Load environment variables from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    logger.error(msg="BOT_TOKEN is not set in the environment variables.")
    exit(1)
bot = telebot.TeleBot(BOT_TOKEN)

# Set up the environment for the LLM model
os.environ["FIREWORKS_API_KEY"] = os.getenv("FIREWORKS_API_KEY")
if os.getenv("FIREWORKS_API_KEY") is None:
    logger.error(msg="FIREWORKS_API_KEY is not set in the environment variables.")
    exit(1)

# Initialize the LLM model
model = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-70b-instruct")

@bot.message_handler(func=lambda message: message)
def respond_and_edit(message):
    # Start with an empty message
    sent_msg = bot.send_message(message.chat.id, "...")

    # Initialize an empty string to accumulate the response
    accumulated_response = ""

    # Generate response using the LLM model and send chunks as they come
    for chunk in model.stream(message.text):

        accumulated_response += chunk.content

        try:
            # Edit the message with the accumulated response
            bot.edit_message_text(accumulated_response, chat_id=message.chat.id, message_id=sent_msg.message_id)
        except Exception:
            continue

def start_bot():
    logger.info(msg=f"Bot `{str(bot.get_me().username)}` has started")
    bot.infinity_polling()
