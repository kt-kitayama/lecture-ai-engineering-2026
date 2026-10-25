"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time
from typing import Any

from google import genai
from google.genai import types, errors

from app.config import MODEL, api_error_message, get_api_key


# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(chat: Any, question: str, temperature: float = 0.0) -> tuple[str, Any, Any, float]:
    # client = genai.Client(api_key=get_api_key())
    # response = client.models.generate_content(model=MODEL, contents=question)

    # TODO(第1回 演習): response.usage_metadata から
    #   入力トークン数と出力トークン数を表示してみよう（Copilotに頼んでよい）

    # 基礎：temperature を設定
    config = types.GenerateContentConfig(temperature = temperature)
    # response = client.models.generate_content(model=MODEL, contents=question, config=config)
    
    # 発展
    """チャットセッションにメッセージを送信し、回答・トークン・時間を返す。"""
    start_time = time.perf_counter()
    response = chat.send_message(question, config=config)
    elapsed_time = time.perf_counter() - start_time

    return (response.text, response.usage_metadata, config, elapsed_time)

# 履歴の中身を表示する関数
def print_chat_history(chat: Any) -> None:
    print("--- [送信されている会話履歴ここから] ---")
    for message in chat.get_history():
        role = "あなた" if message.role == "user" else "AI"
        text = "".join([part.text for part in message.parts if part.text])
        print(f"[{role}]: {text[:80]}...")  # 長い場合は先頭80文字だけ表示
    print("--- [送信されている会話履歴ここまで] ---\n")

def main() -> None:
    parser = argparse.ArgumentParser(description="会話履歴を保ってLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--temp", type=float, default=0.0, help="temperatureの設定")
    args = parser.parse_args()

    # 実装
    client = genai.Client(api_key=get_api_key())
    # 会話履歴を保持するチャットセッションを作成
    chat = client.chats.create(model=MODEL)

    print(f"[model] {MODEL} (temperature={args.temp})")
    print("続けて質問できます（終了するには Enter のみ、または 'exit' / Ctrl+C を入力）\n")

    current_question = args.question
    try:
        while True:
            print(f"[質問] {current_question}\n")

            # どのような内容をLLMへ送っているか確認
            print_chat_history(chat)

            text, usage, config, elapsed = ask(chat, current_question, temperature=args.temp)
            print(f"{text} \n[Temperature]{config.temperature}")

            if usage:
                print(
                    f"\n[Tokens] 入力: {usage.prompt_token_count}, 出力:"
                    f" {usage.candidates_token_count}"
                )
            print(f"[Time] 応答時間: {elapsed:.2f}秒\n")

            # ユーザーからの次の入力を受け付ける
            try:
                user_input = input("> ").strip()
            except EOFError:
                break

            if not user_input or user_input.lower() in ("exit", "quit"):
                break

            current_question = user_input

    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\n終了しました。")

if __name__ == "__main__":
    main()
