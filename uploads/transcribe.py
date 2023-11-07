import pyaudio
import os
import openai

OPENAI_API_KEY_TEMP = "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"

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024)

audio_data = bytes()

try:
    print("Recording... Press Ctrl+C to stop.")
    
    while True:
        # Read audio from the microphone
        data = stream.read(1024)
        print("data:", data)
        audio_data += data
        
except KeyboardInterrupt:
    print("Recording stopped.")
    
finally:
    # Stop PyAudio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

# Transcribe the audio data
# Note: This assumes that the OpenAI API allows for sending audio data directly,
# which might not be the case. You should consult the API documentation.
try:
    transcript = openai.Audio.transcribe("whisper-1", audio_data)
    print("Transcription:", transcript)
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
