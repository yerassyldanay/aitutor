import asyncio
import random
import string
import time
from typing import List

import os
import sys

current_path = os.getcwd()
sys.path.append(current_path)

from constants import env
from gpt.gpt import OpenAIChatGPT
from gpt.gptsession import ChatHistoryStore, Conversation, Platform, Role

class ChatService:
    def __init__(self, chat_history_store: ChatHistoryStore, ai_chat: OpenAIChatGPT):
        self.chat_history_store = chat_history_store
        self.ai_chat = ai_chat

    async def chat(self, role: Role, text: str, session_id: str, current_time: int) -> str:
        # Check if the session_id exists in the database
        conversations = await self.chat_history_store.get_all_by_session(session_id)

        # If the session_id does not exist, create a new conversation
        if not conversations:
            conversations = [Conversation(role, text, current_time)]
        else:
            # If the session_id exists, add the new message to the conversation
            conversations.append(Conversation(role, text, current_time))

        # print(f"\n1.1. conversations: {conversations}\n")

        # Convert conversations to the format expected by OpenAIChatGPT
        messages = [{'role': conv.role.value, 'content': conv.text} for conv in conversations]

        print(f"\nmessages: {messages}\n")

        # Send the messages to OpenAIChatGPT and get the response
        response_text, _ = await self.ai_chat.send_request(messages)

        # Add the AI's response to the chat history
        await self.chat_history_store.add_one(Platform.WEB, session_id, role, text, current_time)

        return response_text

async def main():
    chat_history_store = ChatHistoryStore("./databases/test_db.sql")
    ai_chat = OpenAIChatGPT(env.GPT_API_KEY)
    chat_service = ChatService(chat_history_store, ai_chat)

    # Generate a random session_id
    session_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

    try:
        while True:
            text = input("Enter your message: ")
            response = await chat_service.chat(Role.USER, text, session_id, int(time.time()))
            print(f"AI response: {response}")
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")


if __name__ == "__main__":
    asyncio.run(main())
