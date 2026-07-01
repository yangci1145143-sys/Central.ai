# core/guard.py

import re

def memory_guard(text: str) -> str:
    # 如果回复中编造了“我们昨天/上次/曾经”的虚构记忆，直接拦截
    if re.search(r"(?:我们|你|我)[ ]?(?:昨天|上次|曾经|之前|以前|那一次)", text):
        # 白名单：这些是 Canon 里已有的对话，不拦截
        if "我恐怕连家门都进不去" not in text and "游泳圈" not in text and "喵" not in text:
            return "……我没有这段记忆。你是不是在骗我？"
    return text