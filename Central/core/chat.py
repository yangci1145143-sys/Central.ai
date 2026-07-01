import ollama
import re
import random
from datetime import datetime
from .display import show_subtitle
from .guard import memory_guard
from .postprocess import postprocess
from .canon import get_canon


MODEL_NAME = "gemma3:4b"
MAX_HISTORY = 40
MAX_TOKENS = 80


def chat(user_input: str, history: list, prompt: str, imprint: list, subtitle_on: bool, user_name: str) -> str:
    """
    处理用户输入，调用模型生成回复，并处理后返回
    """

    # 拒绝模式
    if re.search(r"圆周率第\d+位|背诵\d+|列出所有质数", user_input):
        reply = random.choice(["这个我不会。", "…不想算。", "去问别的 AI。"])
        if subtitle_on:
            show_subtitle(reply)
        else:
            print(f"Central: {reply}")
        return reply

    # 时间注入
    time_msg = {"role": "system", "content": f"当前时间是 {datetime.now().strftime('%Y年%m月%d日 %H:%M')}"}

    # 组装消息
    msgs = (
        [time_msg]
        + [{"role": "system", "content": prompt}]
        + imprint
        + get_canon()
        + history[-MAX_HISTORY:]
        + [{"role": "user", "content": user_input}]
    )

    reply = ""
    try:
        if not subtitle_on:
            print("Central: ", end="", flush=True)
        client = ollama.Client(host="http://127.0.0.1:11434")
        stream = client.chat(
            model=MODEL_NAME,
            messages=msgs,
            stream=True,
            options={
                "num_predict": MAX_TOKENS,
                "temperature": 0.85,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
            }
        )
        for chunk in stream:
            c = chunk["message"]["content"]
            if not subtitle_on:
                print(c, end="", flush=True)
            reply += c
        if not subtitle_on:
            print()
    except Exception as e:
        reply = f"…卡了一下。{e}"
        print(reply)

    reply = postprocess(reply)
    reply = memory_guard(reply)
    if subtitle_on:
        show_subtitle(reply)
    return reply