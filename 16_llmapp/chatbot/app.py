import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from graph import build_graph, stream_graph_updates

# 環境変数の読み込み
load_dotenv("../../.env")
os.environ['OPENAI_API_KEY'] = os.environ['API_KEY']

app = Flask(__name__)

# モデル名
MODEL_NAME = "gpt-4o-mini"

# グラフの作成
graph = build_graph(MODEL_NAME)

@app.route('/')
def index():
    """トップページ"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """チャット処理（Web検索連動）"""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')

        if not user_message:
            return jsonify({'error': 'メッセージが空です'}), 400

        # グラフを実行してAIの応答を取得
        response = stream_graph_updates(graph, user_message, session_id)

        return jsonify({
            'response': response,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': f'エラーが発生しました: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
