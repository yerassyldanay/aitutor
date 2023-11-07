
import openai
import streamlit as st
import pyttsx3 

# Initialize the text-to-speech converter
converter = pyttsx3.init() 

# Set the properties for the converter
converter.setProperty('rate', 200)  # Sets speed percent
converter.setProperty('volume', 0.7)  # Set volume 0-1

voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
converter.setProperty('voice', voice_id)  # Use female voice

st.title("ChatGPT-like clone")

openai.api_key = "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"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            chunk_response = response.choices[0].delta.get("content", "")
            full_response += chunk_response
            message_placeholder.markdown(full_response + "▌")

            # converter.say(full_response) 
            # converter.runAndWait()

        message_placeholder.markdown(full_response)
        
        # Convert the assistant's response to speech and play
        converter.say(full_response) 
        converter.runAndWait()
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

