# Web検索連動型チャットボット

LangGraphとTavily Search APIを使用したWeb検索連動型チャットボットです。

## 実装内容

### Chapter 5: オウム返しチャットボット
最初のバージョンとして、ユーザーの入力をそのまま返すシンプルなチャットボットを実装しました。

### Chapter 6: Web検索連動型チャットボット
LangGraphとTavily Search APIを統合し、必要に応じてWeb検索を行うチャットボットに拡張しました。

## 機能

- **LangGraph**: グラフベースのワークフロー管理
- **Tavily Search API**: Web検索機能
- **会話履歴の保持**: セッションごとに会話を記憶
- **自動判断**: 質問に応じて自動的にWeb検索を実行

## 技術スタック

- **バックエンド**: Flask (Python)
- **LLM**: OpenAI GPT-4o-mini
- **フレームワーク**: LangChain, LangGraph
- **検索API**: Tavily Search
- **フロントエンド**: HTML, CSS, JavaScript

## ファイル構成

```
chatbot/
├── app.py                  # Flaskアプリケーション
├── graph.py                # LangGraphのグラフ定義
├── templates/
│   ├── base.html          # ベーステンプレート
│   └── index.html         # メインページ
├── static/
│   └── style.css          # スタイルシート
└── README.md              # このファイル
```

## セットアップ

1. 必要なパッケージをインストール:
```bash
pip install flask python-dotenv langchain langchain-openai langchain-community langgraph
```

2. `.env`ファイルにAPIキーを設定:
```
API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

3. アプリケーションを起動:
```bash
cd 16_llmapp/chatbot
python app.py
```

4. ブラウザで `http://localhost:5000` にアクセス

## 使い方

1. テキストボックスにメッセージを入力
2. 「送信」ボタンをクリック、またはEnterキーを押す
3. チャットボットが回答します
4. 必要に応じて自動的にWeb検索が実行されます

## 動作の流れ

1. ユーザーが質問を入力
2. LangGraphがLLMに質問を送信
3. LLMがツール（Web検索）の必要性を判断
4. 必要であればTavily Search APIでWeb検索を実行
5. 検索結果を元にLLMが回答を生成
6. ユーザーに回答を表示

## 例

**通常の質問**:
- ユーザー: "1たす2は？"
- ボット: "3です。"

**Web検索が必要な質問**:
- ユーザー: "台湾観光について教えて"
- ボット: （Web検索を実行して）台湾の観光情報を提供
