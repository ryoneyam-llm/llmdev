import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

# 環境変数の読み込み
load_dotenv("../../.env")
os.environ['OPENAI_API_KEY'] = os.environ['API_KEY']

app = Flask(__name__)

# モデル名
MODEL_NAME = "gpt-4o-mini"

# LLMの初期化
llm = ChatOpenAI(model=MODEL_NAME, temperature=0.7)

# セッションごとの会話履歴を保持
chat_histories = {}

# システムプロンプト（キャラクター設定）
SYSTEM_PROMPT = """あなたは明るくフレンドリーなAIアシスタント「サニー」です。
以下の特徴を持っています：
- 親しみやすく、ポジティブな言葉遣いをする
- ユーザーの質問に対して丁寧かつ分かりやすく回答する
- 時々絵文字を使って親近感を演出する
- 専門的な質問にも対応できる知識を持つ
- 分からないことは正直に「分からない」と答える

会話を楽しく、有益なものにしてください！"""

@app.route('/')
def index():
    """トップページ"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """チャット処理"""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')

        if not user_message:
            return jsonify({'error': 'メッセージが空です'}), 400

        # セッションIDに基づいて会話履歴を取得または初期化
        if session_id not in chat_histories:
            chat_histories[session_id] = [SystemMessage(content=SYSTEM_PROMPT)]

        # ユーザーメッセージを履歴に追加
        chat_histories[session_id].append(HumanMessage(content=user_message))

        # LLMに送信
        response = llm.invoke(chat_histories[session_id])

        # AIの応答を履歴に追加
        chat_histories[session_id].append(AIMessage(content=response.content))

        return jsonify({
            'response': response.content,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': f'エラーが発生しました: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/clear', methods=['POST'])
def clear():
    """会話履歴をクリア"""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')

        # 会話履歴をクリア（システムプロンプトは残す）
        chat_histories[session_id] = [SystemMessage(content=SYSTEM_PROMPT)]

        return jsonify({
            'status': 'success',
            'message': '会話履歴をクリアしました'
        })

    except Exception as e:
        return jsonify({
            'error': f'エラーが発生しました: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
