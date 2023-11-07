import os
import openai
import sounddevice as sd
import numpy as np
import webrtcvad
import queue

# Set the OpenAI API Key
OPENAI_API_KEY_TEMP = "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"
openai.api_key = os.getenv(OPENAI_API_KEY_TEMP)

# Initialize VAD (Voice Activity Detection)
vad = webrtcvad.Vad(2)

# Queue to store audio blocks
q = queue.Queue()
silence_counter = 0
silence_threshold = 16
q_threshold = 16

def audio_callback(indata, frames, time, status):
    global silence_counter

    if status:
        print(f"underlying audio stack warning: {status}")

    audio_data = map(lambda x: (x + 1) / 2, indata)  # normalize from [-1,+1] to [0,1]
    audio_data = list(audio_data)  # Convert map object to list
    print(np.shape(audio_data))  # Debug: print the shape of audio_data
    audio_data = np.fromiter(audio_data, np.float16)

    audio_data = audio_data.tobytes()
    print(len(audio_data))  # Debug: print the length of audio_data
    try:
        detection = vad.is_speech(audio_data, 16000)  # Assuming a 16kHz sample rate
        if detection:
            q.put(indata.copy())
            silence_counter = 0
        else:
            if silence_counter >= silence_threshold:
                if q.qsize() > q_threshold:
                    transcribe_speech()
                    silence_counter = 0
            else:
                silence_counter += 1
    except Exception as e:
        print(f"Error in VAD: {str(e)}")

def transcribe_speech():
    print("Transcribing speech ...")
    audio_data = np.array([])
    while q.qsize() > 0:
        audio_data = np.append(audio_data, q.get())
    audio_data = np.concatenate([audio_data, np.zeros((int(16000) + 10))])

    # Convert the NumPy array to bytes
    audio_bytes = audio_data.tobytes()
    
    # Use OpenAI's Whisper AI to transcribe the audio
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_bytes)
        print("Transcription:", transcript)
    except Exception as e:
        print(f"An error occurred while transcribing: {str(e)}")

    
# Use the sounddevice library to record audio
with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000):
    print("Recording... Press Ctrl+C to stop.")
    while True:
        pass