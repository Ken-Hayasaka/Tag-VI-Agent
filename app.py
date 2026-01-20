import os
import streamlit as st
import google.generativeai as genai

# --- ページ設定 ---
st.set_page_config(
    page_title="Tag-VI Agent",
    page_icon="🧠",
    layout="wide"
)

# --- タイトルと説明 ---
st.title("🧠 構造化思考エージェント Tag-VI")
st.markdown("""
あなたの悩みや課題を入力してください。
独自プロトコル**「認知分類法タグ6層」**に基づき、構造的な分析と本質的な解決策を提示します。
""")

# --- APIキーの取得 ---
# Cloud Runなどの環境変数からキーを読み込む安全な設計
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ APIキーが設定されていません。環境変数 GOOGLE_API_KEY を設定してください。")
    st.stop()

# --- Geminiの設定 ---
genai.configure(api_key=api_key)

# システムプロンプト（タグ6層の定義）
SYSTEM_PROMPT = """
{
  "protocol_name": "Cognitive_Tagging_6Layers",
  "description": "Information structuring protocol to minimize semantic drift and hallucinations.",
  "layers": {
    "L1_Surface": {
      "desc": "Category or Topic",
      "example": ["AI", "Economics"]
    },
    "L2_Structure": {
      "desc": "Mechanism, Causality, Pattern",
      "example": ["Integration", "Feedback Loop"]
    },
    "L3_Context": {
      "desc": "Time, Culture, History",
      "example": ["2025s", "Post-Modern"]
    },
    "L4_Philosophy": {
      "desc": "Values, Beliefs, Ethics",
      "example": ["Rationality", "Open Source Spirit"]
    },
    "L5_Cognition": {
      "desc": "Sensation, Aesthetic, Vibe",
      "example": ["Immersive", "Minimalist"]
    },
    "L6_Meta": {
      "desc": "Operational Rules",
      "example": ["Use Python", "Output as JSON"]
    }
  },
  "instruction": "Analyze the user input based on these 6 layers before generating a response. Output must include specific analysis for each layer (L1-L6) and a final structural conclusion."
}
"""

# モデルの準備
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # 高速で安定しているモデルを指定
    system_instruction=SYSTEM_PROMPT
)

# --- チャット画面の構築 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去の履歴を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力
if prompt := st.chat_input("例：現場の職人がなかなか新しいツールを使ってくれない…"):
    # ユーザーの入力を表示
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AIの応答生成
    with st.chat_message("assistant"):
        with st.spinner("タグ6層プロトコルで構造解析中..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
