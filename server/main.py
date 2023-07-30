import os
import random
import string
import sys
import time

from quart import Quart, render_template, request, jsonify, redirect, url_for
from urllib.parse import parse_qs

current_path = os.getcwd()
sys.path.append(current_path)

from constants import env, variables
from gpt.gpt import OpenAIChatGPT
from gpt.gptsession import ChatHistoryStore, Role
from server.service.chat import ChatService

app = Quart(__name__)

chat_history_store = ChatHistoryStore("./databases/web_db.sql")
open_ai_api = OpenAIChatGPT(env.GPT_API_KEY)
chat_service = ChatService(chat_history_store, open_ai_api)

@app.route('/chat', methods=['GET', 'POST'])
async def chat():
    if request.method == "GET":
        return redirect(url_for('home'))

    data = await request.get_data()
    parsed_data = parse_qs(data.decode())
    name = parsed_data.get('name', ['Yerassyl'])[0]
    text = variables.DESCRIPTION % name

    # Generate a random session_id
    session_id = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(32))
    session_id = "web_" + session_id

    # Get the current time
    current_time = int(time.time())

    # Call the chat method
    response = await chat_service.chat(Role.SYSTEM, text, session_id, current_time)
    # response = "This is a response"

    # Render the chat template with the response
    return await render_template('chat.html', name=name, session_id=session_id, messages=[{'role': 'ai', 'text': response}])

@app.route('/message', methods=['POST'])
async def message():
    # Get the data from the request
    data = await request.get_json()
    session_id = data.get('session_id')
    text = data.get('text')

    print(f'Received message from session {session_id}: {text}')

    if not session_id or not text:
        return redirect(url_for('home'))

    # Get the current time
    current_time = int(time.time())

    # Call the chat method
    response_text = await chat_service.chat(Role.USER, text, session_id, current_time)

    # Return the response
    return jsonify({'text': response_text})


@app.route('/')
async def home():
    return await render_template('welcome.html')


if __name__ == '__main__':
    app.run(debug=True)
