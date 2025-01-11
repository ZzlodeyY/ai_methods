import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import load_config
from handlers import handle_start_command, handle_callback_query, handle_user_message
from models import ModelManager


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    config = load_config()
    ModelManager.initialize(config) 
    application = Application.builder().token(config.tg_token).build()

   
    application.add_handler(CommandHandler("start", handle_start_command))
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

   
    application.run_polling()

if __name__ == "__main__":
    main()