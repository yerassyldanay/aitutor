from telegram import Update

class Utility:
    @staticmethod
    def get_user_info(update: Update) -> dict:
        user_info = dict()
        chat = None
        if hasattr(update, 'callback_query') and update.callback_query != None \
            and hasattr(update.callback_query, 'message') and update.callback_query.message != None \
            and hasattr(update.callback_query.message, 'chat') and update.callback_query.message.chat != None:
            chat = update.callback_query.message.chat
        elif update.message != None and update.message.chat != None:
            chat = update.message.chat
        else:
            return user_info

        if chat.first_name:
            user_info['first_name'] = chat.first_name
        
        if chat.username:
            user_info['username'] = chat.username
        
        if chat.id:
            user_info['id'] = chat.id

        if chat.type:
            user_info['type'] = chat.type

        return user_info
