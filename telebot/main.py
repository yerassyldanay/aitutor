import asyncio
import logging
from typing import List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, Chat
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    PicklePersistence,
    CommandHandler,
    ConversationHandler,
)

from gpt import env, constants
from gpt.gpt import OpenAIChatGPT
from utils.utils import Utility

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

ENGLISH_LEVEL = "english"
MESSAGES = "messages"

class Application(Utility):
    NUMBER_OF_MSG_TO_CONSIDER = 3

    def __init__(self) -> None:
        self.__persistence = PicklePersistence(filepath="arbitrarycallbackdatabot")
        self.bot = Bot(env.BOT_TOKEN_AI_TUTOR)
        self.application = ApplicationBuilder().persistence(self.__persistence).token(env.BOT_TOKEN_AI_TUTOR).concurrent_updates(True).build()
        self.gpt = OpenAIChatGPT(env.GPT_API_KEY)
        self.__set_buttons__()
    
    def __set_buttons__(self):
        startCommand = CommandHandler("start", self.__start__)
        conversation = ConversationHandler(
            entry_points=[
                startCommand,   
            ],
            states={},
            fallbacks=[
                startCommand,
            ]
        )
        self.application.add_handler(conversation)
    
    async def __start__(self, update: Update, context: CallbackContext):
        context.user_data[ENGLISH_LEVEL] = constants.EnglishLevel.Intermediate
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode="HTML", 
            text=constants.Msg.CHOOSE_ENGLISH_LEVEL,
            reply_markup=constants.EnglishLevel.Buttons,
        )

        return constants.STATE.CHOOSE_ENGLISH_LEVEL

    async def __choose_english_level__(self, update: Update, context: CallbackContext):
        chosen_english_level = update.callback_query.data
        if not chosen_english_level.startswith("choose_english_level_"):
            self.__start__(update, context)
            return constants.STATE.CHOOSE_ENGLISH_LEVEL
        
        chosen_english_level = chosen_english_level.replace("choose_english_level_", "").upper()
        if chosen_english_level in constants.EnglishLevel.LEVEL_MAP:
            context.user_data[ENGLISH_LEVEL] = constants.EnglishLevel.LEVEL_MAP[chosen_english_level]
        else:
            context.user_data[ENGLISH_LEVEL] = constants.EnglishLevel.Intermediate

        level = context.user_data[ENGLISH_LEVEL]
        description = constants.DESCRIPTION % '/'.join(list(level))

        resp = await self.gpt.send_request()
        if resp is not None and len(resp) == 2:
            # 1. need to get MESSAGES from context.user_data
            # 2. add user's input as 
            # {
            #     "role": "system",
            #     "content": user's input,
            # },
            # 3. restore it
            # 4. 
            pass

        return constants.STATE.TALK_TO_AI

    async def __message__(self, update: Update, context: CallbackContext):
        msg = update.message.text
        logger.info(f"user {update.message.from_user.id} / {update.message.from_user.username} " + \
                    f"new {update.message.text}")
        pass

    async def __get_messages__(self, update: Update, context: CallbackContext) -> List:
        level = context.user_data.get(ENGLISH_LEVEL, constants.EnglishLevel.Intermediate)
        messages_to_send = [
            {
                "role": "system",
                "content": constants.DESCRIPTION % '/'.join(list(level)),
            },
        ]
        messages = context.user_data.get(MESSAGES, []).copy()
        if len(messages) > self.NUMBER_OF_MSG_TO_CONSIDER:
            messages = messages[-self.NUMBER_OF_MSG_TO_CONSIDER:]
        messages_to_send.extend(messages)
        return messages_to_send

    def run(self):
        self.application.run_polling()

    async def __close(self):
        return asyncio.gather(self.application.shutdown())

    def close(self):
        asyncio.run(self.__close())


if __name__ == '__main__':
    app = Application()
    try:
        app.run()
    except Exception as ex:
        print(ex)
    finally:
        app.close()
