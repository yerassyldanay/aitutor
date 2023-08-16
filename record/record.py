import speech_recognition as sr

# Create an instance of the Recognizer class
r = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    # Read the audio data from the microphone
    print('Start speaking...')
    audio_data = r.record(source, duration=10)
    # Convert speech to text
    text = r.recognize_google(audio_data)
    print(text)
