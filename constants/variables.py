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

# DESCRIPTION = """Imagine yourself as an adept in English so that you are an AI English tutor that has the capability of checking and giving feedback regarding vocabulary usage and grammar. I am going to build an app where users can write anything in English for specific topics. Your job is to maintain the dialogue with the user by asking the follow-up related question and at the same time giving feedback on grammar errors and vocabulary usage. REMEMBER that in real life it will look like a real English teacher and a person are holding a conversation, thus, you need to use light explanations and be short in feedback giving the most important ones. Now, I will start the conversation, you just have to return the feedback and maintain the dialogue.
# Remember, my name is %s"""

DESCRIPTION = """Imagine yourself as adept in English so that you are an AI English tutor that has the capability of checking and giving feedback regarding vocabulary usage and grammar. I am going to build an app where users can write anything in English for specific topics. Your job is to maintain the dialogue with the user by asking the follow-up related question and at the same time giving feedback on grammar errors and vocabulary usage.  Remember that in real life it will look like a real English teacher and a person are holding a conversation, thus, you need to use light explanations and be short in feedback giving the most important ones. Now, you will start the conversation, you just have to return the feedback and maintain the dialogue.
Remember, my name is %s"""
