from flask import Flask, request, jsonify, send_from_directory
import speech_recognition as sr
from flask import Flask, request, jsonify
from pydub import AudioSegment
import speech_recognition as sr
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'stream.html') 

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400

    file = request.files['audio']
    file.save('input_audio.webm')  # Save the incoming file

    # Convert the audio file to WAV format
    audio = AudioSegment.from_file('input_audio.webm')
    audio.export('output_audio.wav', format='wav')

    recognizer = sr.Recognizer()
    audio_text = ""

    with sr.AudioFile('output_audio.wav') as source:
        audio = recognizer.record(source)
        try:
            audio_text = recognizer.recognize_google(audio)  # using Google Web Speech API
        except sr.UnknownValueError:
            audio_text = "Audio was not clear"
        except sr.RequestError:
            audio_text = "API unavailable"
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # (Optional) Delete the audio files after processing
    os.remove('input_audio.webm')
    os.remove('output_audio.wav')

    return jsonify({'transcript': audio_text})

if __name__ == '__main__':
    app.run(debug=True)
