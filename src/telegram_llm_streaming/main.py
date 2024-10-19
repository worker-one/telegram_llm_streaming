from telegram_llm_streaming.api.bot import start_bot
from telegram_llm_streaming.db.database import create_tables, db_avaliable

if __name__ == "__main__":
    if db_avaliable:
        create_tables()
    start_bot()
