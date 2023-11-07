from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import logging
import os

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS

logging.basicConfig(level=logging.INFO)  # Enable logging

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'button.html')  # make sure 'button.html' exists in the 'static' directory

@socketio.on('connect')
def handle_connect():
    logging.info("Client connected: {}".format(request.sid))

@socketio.on('disconnect')
def handle_disconnect():
    logging.info("Client disconnected: {}".format(request.sid))

@socketio.on('message')
def handle_message(message):
    logging.info("Received message: {}".format(message))
    # Here, you would add the logic to process the audio chunk, such as sending it to a speech-to-text service.
    # Then, you could emit a response back to the client with the transcribed text.
    try:
        # Assuming the message is the binary audio data, we need to write it to a file before recognition
        with open("temporary_audio.wav", "wb") as file:
            file.write(message)

        recognizer = sr.Recognizer()
        with sr.AudioFile("temporary_audio.wav") as source:
            audio_data = recognizer.record(source)  # read the entire audio file

        # Recognizing the content from the audio file
        text = recognizer.recognize_google(audio_data)
        emit('message', text)  # Sending transcribed text back to client

        # Optionally, delete the temporary file
        os.remove("temporary_audio.wav")

    except Exception as e:
        logging.error("Error: {}".format(e))
        emit('message', str(e))  # Sending error message back to client

if __name__ == '__main__':
    # Use 'socketio.run' instead of 'app.run' for starting the SocketIO server
    socketio.run(app, debug=True, port=5000)
