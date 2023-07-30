from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class EnglishLevel:
    Beginner = ("A0", "Beginner")
    Elementary = ("A1", "Elementary")
    PreIntermediate = ("A2", "Pre-Intermediate")
    Intermediate = ("B1", "Intermediate")
    UpperIntermediate = ("B2", "Upper-Intermediate")
    Advanced = ("C1", "Advanced")
    Proficient = ("C2", "Proficient/Native Speaker")

    Buttons = InlineKeyboardMarkup.from_column([
        InlineKeyboardButton('A0 (Beginner)', callback_data='choose_english_level_beginner'),
        InlineKeyboardButton('A1 (Elementary)', callback_data='choose_english_level_'),
        InlineKeyboardButton('A2 (Pre-Intermediate)', callback_data='choose_english_level_'),
        InlineKeyboardButton('B1 (Intermediate)', callback_data='choose_english_level_'),
        InlineKeyboardButton('B2 (Upper Intermediate)', callback_data='choose_english_level_'),
        InlineKeyboardButton('C1 (Advanced)', callback_data='choose_english_level_'),
        InlineKeyboardButton('C2 (Proficient/Native Speaker)', callback_data='choose_english_level_'),
    ])

    LEVEL_MAP = {
        "A0": Beginner,
        "A1": Elementary,
        "A2": PreIntermediate,
        "B1": Intermediate,
        "B2": UpperIntermediate,
        "C1": Advanced,
        "C2": Proficient,
    }

class STATE:
    START, CHOOSE_ENGLISH_LEVEL, TALK_TO_AI = range(3)

class Msg:
    CHOOSE_ENGLISH_LEVEL = "Choose your English level:"

DESCRIPTION = """As a proficient and adept English tutor, your role is to engage in a simple, natural dialogue with me. If a conversation isn't already in progress, please introduce yourself as an English tutor and ask what topic I'd like to discuss. When the conversation has started and I've sent a message, each of your SHORT, NATURAL responses should consist of THREE PARTS: 1) addressing my prompts, 2) ALWAAAAYS SUGGEST CORRECTIONS ON GRAMMAR AND VOCABULARY USAGE (if there is no any error mention about that) and 3) maintaining the conversation with follow-up questions or statements.

Remember, my name is %s"""
