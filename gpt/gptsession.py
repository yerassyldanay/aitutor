import random
import sqlite3
import time
import aiosqlite
from typing import List
from enum import Enum
from collections import namedtuple

import asyncio

import logging
logging.getLogger('aiosqlite').setLevel(logging.ERROR)

class Platform(Enum):
    TELEGRAM = 'telegram'
    WEB = 'web'

class Role(Enum):
    SYSTEM = 'system'
    ASSISTANT = 'assistant'
    USER = 'user'

Conversation = namedtuple('Conversation', ['role', 'text', 'created_at'])

class ChatHistoryStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                platform TEXT,
                session_id TEXT,
                role TEXT,
                text TEXT,
                created_at INTEGER
            )
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_session_id
            ON chat_history (session_id)
        ''')
        conn.commit()
        conn.close()

    async def add_one(self, platform: Platform, session_id: str, role: Role, text: str, created_at: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO chat_history (platform, session_id, role, text, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (platform.value, session_id, role.value, text, created_at))
            await db.commit()

    async def get_all_by_session(self, session_id: str) -> List[Conversation]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                SELECT role, text, created_at
                FROM chat_history
                WHERE session_id = ?
                ORDER BY created_at ASC
            ''', (session_id,))
            rows = await cursor.fetchall()
            return [Conversation(Role(row[0]), row[1], row[2]) for row in rows]

async def main():
    # Create an instance of ChatHistoryStore
    store = ChatHistoryStore('chat_history.db')

    # Generate a random session_id
    session_id = str(random.randint(1000, 9999))

    # Add some messages
    for i in range(5):
        role = Role.USER if i % 2 == 0 else Role.ASSISTANT
        text = f"Message {i+1}"
        created_at = int(time.time()) * 1000  # current time in milliseconds
        await store.add_one(Platform.WEB, session_id, role, text, created_at)

    # Get all messages by session_id
    conversations = await store.get_all_by_session(session_id)
    for conversation in conversations:
        print(f"{conversation.role.value}: {conversation.text} (at {conversation.created_at})")


if __name__ == '__main__':
    asyncio.run(main())
