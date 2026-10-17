
import json
import streamlit as st
import utils_sat


st.title('OFFLINE CHATBOT')

CHAT_FILE = 'chat_history.json'
SUMMARY_FILE = 'chat_summary.txt'

WELCOME_MSG = {'role': 'ai', 'content': 'How Can I Help YOU?'}


model = 'gemma3:1b'


def load_history():
    f = open(CHAT_FILE, 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


def save_history(messages):
    f = open(CHAT_FILE, 'w', encoding='utf-8')
    json.dump(messages, f, ensure_ascii=False, indent=2)
    f.close()


def clear_history():
    open(CHAT_FILE, 'w', encoding='utf-8').close()
    open(SUMMARY_FILE, 'w', encoding='utf-8').close()



if 'messages' not in st.session_state:
    st.session_state['messages'] = [WELCOME_MSG.copy()]

if 'stop' not in st.session_state:
    st.session_state['stop'] = False



col1, col2, col3 = st.columns(3)

with col1:
    
    if st.button('[-]Stop'):
        st.session_state['stop'] = True
        st.warning('مدل متوقف شد.')

with col2:

    if st.button('[+]continue'):
        st.session_state['stop'] = False
        st.success('مدل فعال شد.')
        st.rerun()

with col3:
    if st.button('cleaner'):
        st.session_state['messages'] = [WELCOME_MSG.copy()]
        st.session_state['stop'] = False
        clear_history()
        st.rerun()


for msg in st.session_state['messages']:
    st.chat_message(msg['role']).write(msg['content'])

prompt = st.chat_input('Ask Your Question')

if prompt:

    if st.session_state['stop']:
        st.error('stoping............................')

    else:
        st.chat_message('user').write(prompt)
        st.session_state['messages'].append({'role': 'user', 'content': prompt})


        with st.spinner(' Answer...'):
            response = utils_sat.call_ollama_model(prompt, model)

        st.chat_message('ai').write(response)
        st.session_state['messages'].append({'role': 'ai', 'content': response})

        save_history(st.session_state['messages'])


if st.button('! خلاصه کردن چت'):

    if len(st.session_state['messages']) > 1:

        summary = f"""
        .این گفتگو زیر را به فارسی خلاصه کن

        متن گفتگو:
        {st.session_state['messages']}
        """

        with st.spinner('در حال خلاصه‌سازی...'):
            summary = utils_sat.call_ollama_model(summary, model)

        f = open(SUMMARY_FILE, 'w', encoding='utf-8')
        f.write(summary)
        f.close()



        st.success('خلاصه سیو شد .')
        st.write(summary)

    else:
        st.warning('چتی برای خلاصه کردن وجود ندارد.')