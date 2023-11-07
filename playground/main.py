import openai
import streamlit as st

import os, sys

current_path = os.getcwd()
sys.path.append(current_path)

from playground import prompt

st.title("Omni Talk")

openai.api_key = "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"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar options
options = list(prompt.MAP_NAMES.keys())
st.sidebar.header("Choose an option:")

st.session_state["changed"] = st.session_state.get("changed", False)
# Using buttons instead of a selectbox
selected_option = st.session_state.get("selected_option", "")
for option in options:
    if st.sidebar.button(option):
        print("hit:", option)
        st.session_state["changed"] = True
        selected_option = option
        st.session_state.selected_option = selected_option  # Store the selected option in session_state

# Display the selected option and related message outside of the loop
if selected_option and st.session_state.get("changed", False):
    st.session_state["changed"] = False
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": prompt.MAP_NAMES[selected_option]})

for message in st.session_state.messages:
    if message.get("role") == "system":
        continue
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
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
