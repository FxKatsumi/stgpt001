import openai
import streamlit as st
from PIL import Image

from persons import personality, getPerson

# セッションの初期化
if 'texts' not in st.session_state:
    st.session_state.texts = [] # 質問履歴
if 'messages' not in st.session_state:
    st.session_state.messages = [] # メッセージ履歴

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

    try:
        if len(past_messages) == 0 and len(settings_text) != 0:
            system = {"role": "system", "content": settings_text}
            past_messages.append(system)
        new_message = {"role": "user", "content": new_message_text}
        past_messages.append(new_message)

        # Open AI Key
        openai.api_key = st.secrets.openai_settings.openai_key

        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=past_messages
        )
        response_message = {"role": "assistant", "content": result.choices[0].message.content}
        past_messages.append(response_message)
        response_message_text = result.choices[0].message.content

        return response_message_text, past_messages

    except Exception as e:
        pass

# メイン処理
def appmain():
    try:
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
        
        st.sidebar.write("") # 改行

        # ロゴマーク表示
        img = Image.open('images/forex_logo_a.png')
        st.sidebar.image(img, width=150, use_column_width=False)

        # メイン画面

        # st.title('〇〇チャットボット')
        # st.title('なりきりチャットボット')
        st.title('なりきりくん')
        st.caption('Powered by chatGPT')

        # 入力フォーム
        with st.form("my_form", clear_on_submit=True): # 毎回テキストボックスをクリア
            # text = st.text_input('新しい質問：', '')
            text = st.text_area('新しい質問：', '')
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
        c = 0
        for t in reversed(st.session_state.texts):
            if c == 1: # 回答？
                # st.subheader(t) # 文字を大きく
                st.markdown(f'<span style="color:green;">{t}</span>', unsafe_allow_html=True) # 緑色
            else:
                st.write(t)

            c = c + 1 # インクリメント

    except Exception as e:
        st.error("エラー：" + str(e))

#コマンドプロンプト上で表示する
if __name__ == "__main__":
    #メイン処理
    appmain()
