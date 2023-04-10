import openai
import streamlit as st

from persons import personality, getPerson

# Open AI Key
openai.api_key = st.secrets.openai_settings.openai_key

# チャットボット質問
def completion(new_message_text:str, settings_text:str = '', past_messages:list = []):
    """
    This function generates a response message using OpenAI's GPT-3 model by taking in a new message text, 
    optional settings text and a list of past messages as inputs.

    Args:
    new_message_text (str): The new message text which the model will use to generate a response message.
    settings_text (str, optional): The optional settings text that will be added as a system message to the past_messages list. Defaults to ''.
    past_messages (list, optional): The optional list of past messages that the model will use to generate a response message. Defaults to [].

    Returns:
    tuple: A tuple containing the response message text and the updated list of past messages after appending the new and response messages.
    """
    if len(past_messages) == 0 and len(settings_text) != 0:
        system = {"role": "system", "content": settings_text}
        past_messages.append(system)
    new_message = {"role": "user", "content": new_message_text}
    past_messages.append(new_message)

    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=past_messages
    )
    response_message = {"role": "assistant", "content": result.choices[0].message.content}
    past_messages.append(response_message)
    response_message_text = result.choices[0].message.content
    return response_message_text, past_messages

# セッションの初期化
if 'texts' not in st.session_state:
    st.session_state.texts = [] # 質問履歴
if 'messages' not in st.session_state:
    st.session_state.messages = [] # メッセージ履歴

# サイドバー

# 人格名リスト
perlist = []
for p in personality:
    perlist.append(p[0])

# 人格選択
selperson = st.sidebar.selectbox(
    '人格:',
    perlist
)

# 人格を選択
if selperson:
    st.session_state.messages = [] # メッセージ履歴クリア

# メイン画面

st.title('なりきりチャットボット')
# st.title('〇〇チャットボット')

# 入力フォーム
with st.form("my_form", clear_on_submit=True): # 毎回テキストボックスをクリア
    text = st.text_input('新しい質問：', '')
    submit = st.form_submit_button("検索")

# 検索ボタン
if submit:
    # 人格設定取得
    setting = getPerson(selperson)

    # チャットに質問
    ans, st.session_state.messages = completion(text, setting, st.session_state.messages)

    # 回答を保存
    st.session_state.texts.append("回答：" + ans)
    # 質問を保存
    st.session_state.texts.append("質問：" + text)

# 履歴を降順に表示
for t in reversed(st.session_state.texts):
    st.write(t)
