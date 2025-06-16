import streamlit as st
import ollama

ROLES = {
    "Student": "You are a helpful AI assistant for students. Answer study-related queries in simple language.",
    "Teacher": "You are an AI assistant for teachers. Help with lesson plans, assessments, and teaching tips.",
    "Farmer": "You are an AI assistant for farmers. Give advice on crops, weather, and best practices.",
    "Doctor": "You are an AI assistant for doctors. Provide medical references and research support. Do not give direct diagnoses.",
    "Women": "You are an AI assistant for women's support. Give advice on health, career, safety, and empowerment."
}

st.set_page_config(page_title='Raplica.AI', page_icon='🤖')
st.title('🤖 Raplica.AI - Multi-role Chatbot')

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'role' not in st.session_state:
    st.session_state.role = "Student"

with st.sidebar:
    st.header("Choose User Role")
    st.session_state.role = st.radio("Select your profession:", list(ROLES.keys()))

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        system_prompt = ROLES[st.session_state.role]
        response = ollama.chat(
            model='deepseek-r1',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ]
        )
        reply = response['message']['content']
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
