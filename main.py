import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from settings import TOKEN, GROUP
from emails import emails

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def error_formater(error_message: str, function_name: str) -> str:
    return (
        "=" * 8
        + f"ERROR RAISED INSIDE {function_name}"
        + "=" * 8
        + f"\n {error_message}"
    )


def generate_welcome_message(username: str) -> str:

    # * * bold text
    # Refer for more https://developers.sinch.com/docs/conversation/channel-support/telegram/markdown/#:~:text=You%20can%20use%20Markdown%20to,on%20the%20Telegram%20Bot%20channel.
    return f"Welcome *{username}* \n1\. Use /add to add project"


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        bot = context.bot
        chat_id = update.message.chat_id
        text = generate_welcome_message(username=update.message.from_user.first_name)

        await bot.send_message(chat_id=chat_id, text=text, parse_mode="MarkdownV2")

    except Exception as e:
        logger.log(
            level=logging.ERROR,
            msg=error_formater(error_message=e, function_name="start_handler"),
        )


async def add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    try:
        bot = context.bot
        chat_id = update.message.chat_id
        topic_name = update.message.text[4:]

        await bot.create_forum_topic(chat_id=GROUP, name=topic_name)

    except Exception as e:
        logger.log(
            level=logging.ERROR,
            msg=error_formater(error_message=e, function_name="add_handler"),
        )
        await bot.send_message(
            chat_id=chat_id, text="Sorry, can't add project at the moment!"
        )


async def edit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        bot = context.bot
        chat_id = update.message.chat_id
        new_topic_name = update.message.text[5:]

        await bot.edit_forum_topic(
            chat_id=GROUP, message_thread_id=4, name=new_topic_name
        )

    except Exception as e:
        logger.log(
            level=logging.ERROR,
            msg=error_formater(error_message=e, function_name="edit_handler"),
        )
        await bot.send_message(
            chat_id=chat_id, text="Sorry, can't edit project at the moment!"
        )


async def delete_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        bot = context.bot
        chat_id = update.message.chat_id

        await bot.delete_forum_topic(chat_id=GROUP, message_thread_id=4)

    except Exception as e:
        logger.log(
            level=logging.ERROR,
            msg=error_formater(error_message=e, function_name="edit_handler"),
        )
        await bot.send_message(
            chat_id=chat_id, text="Sorry, can't edit project at the moment!"
        )


async def emails_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        bot = context.bot
        chat_id = update.message.chat_id

        await bot.send_message(chat_id=chat_id, text=emails)

    except Exception as e:
        logger.log(
            level=logging.ERROR,
            msg=error_formater(error_message=e, function_name="emails_handler"),
        )
        await bot.send_message(
            chat_id=chat_id, text="Sorry, can't get emails at the moment!"
        )


async def id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    print(f"chat_id {update.message.chat_id}")
    try:
        print(f"thread_id {update.message.message_thread_id}")
    except:
        pass


def main() -> None:

    # Initializing bot
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("add", add_handler))
    application.add_handler(CommandHandler("edit", edit_handler))
    application.add_handler(CommandHandler("delete", delete_handler))
    application.add_handler(CommandHandler("emails", emails_handler))
    application.add_handler(CommandHandler("id", id_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
