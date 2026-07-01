import sys
import os
from datetime import datetime

from core.chat import chat
from core.config import load_config, save_config
from core.memory import load_memory, save_memory, load_important, save_important
from core.display import show_subtitle
from core.festival import get_festival
from core.prompt import build_prompt, build_imprint


def main():

    cfg = load_config()
    if not cfg:
        cfg = setup_first_run()

    user_name = cfg.get("user_name", "Cas9")
    user_birthday = cfg.get("user_birthday", "未知")
    subtitle_on = cfg.get("subtitle", True)


    history = load_memory()
    important = load_important()
    imprint = build_imprint()
    prompt = build_prompt(user_name, user_birthday, important)

    today = datetime.now().strftime("%m-%d")
    festival = get_festival(today)

    print("\n" + "=" * 50)
    print(f"  Central V0.75  |  你好，{user_name}")
    print(f"  字幕: {'ON' if subtitle_on else 'OFF'}")
    print("  /clear /history /remember /forget /subtitle /id /exit")
    print("=" * 50 + "\n")

    if festival:
        show_subtitle(festival) if subtitle_on else print(f"Central: {festival}")
    if user_birthday == today:
        msg = f"…今天是你生日。生日快乐，{user_name}。"
        show_subtitle(msg) if subtitle_on else print(f"Central: {msg}")

    while True:
        try:
            user_input = input(f"{user_name} > ").strip()
            if not user_input:
                continue

            if user_input == "/exit":
                save_memory(history)
                save_important(important)
                show_subtitle("…走了啊。") if subtitle_on else print("Central: …走了啊。")
                break

            elif user_input == "/clear":
                history = []
                save_memory(history)
                print("Central: 嗯 那就翻篇了\n")

            elif user_input == "/history":
                if not history:
                    print("没有记录。\n")
                else:
                    print("\n" + "-" * 30)
                    for m in history[-10:]:
                        role = user_name if m['role'] == 'user' else 'Central'
                        print(f"{role}: {m['content'][:60]}")
                    print("-" * 30 + "\n")

            elif user_input == "/remember":
                print(f"重要记忆（{len(important)}/5）：")
                for i, item in enumerate(important):
                    print(f"  {i+1}. {item}")
                note = input("添加记忆（跳过回车）> ").strip()
                if note:
                    if len(important) >= 5:
                        print("已满5条，请先用 /forget 删除一条。")
                    else:
                        important.append(note)
                        save_important(important)
                        prompt = build_prompt(user_name, user_birthday, important)
                        print("已记录。\n")

            elif user_input == "/forget":
                if not important:
                    print("没有重要记忆。\n")
                else:
                    for i, item in enumerate(important):
                        print(f"  {i+1}. {item}")
                    idx = input("删除哪条？（输入编号）> ").strip()
                    if idx.isdigit() and 1 <= int(idx) <= len(important):
                        removed = important.pop(int(idx) - 1)
                        save_important(important)
                        prompt = build_prompt(user_name, user_birthday, important)
                        print(f"已删除：{removed}\n")

            elif user_input == "/subtitle":
                subtitle_on = not subtitle_on
                cfg["subtitle"] = subtitle_on
                save_config(cfg)
                print(f"字幕: {'ON' if subtitle_on else 'OFF'}\n")

            elif user_input == "/id":
                print(f"\n名字：{user_name}  生日：{user_birthday}")
                new_name = input("新名字（跳过回车）> ").strip()
                new_bd = input("新生日 MM-DD（跳过回车）> ").strip()
                changed = False
                if new_name:
                    cfg["user_name"] = new_name
                    user_name = new_name
                    changed = True
                if new_bd:
                    cfg["user_birthday"] = new_bd
                    user_birthday = new_bd
                    changed = True
                if changed:
                    save_config(cfg)
                    prompt = build_prompt(user_name, user_birthday, important)
                    print("Central: …好。\n")
                else:
                    print("没有改动。\n")

            else:
                reply = chat(
                    user_input=user_input,
                    history=history,
                    prompt=prompt,
                    imprint=imprint,
                    subtitle_on=subtitle_on,
                    user_name=user_name
                )
                history.append({"role": "user", "content": user_input})
                history.append({"role": "assistant", "content": reply})
                save_memory(history)

        except KeyboardInterrupt:
            save_memory(history)
            save_important(important)
            print("\nCentral: …走了啊。")
            break

def setup_first_run() -> dict:
    print("\n" + "=" * 40)
    print("  第一次启动 Central")
    print("=" * 40 + "\n")
    user_name = input("你叫什么名字？> ").strip() or "Cas9"
    user_birthday = input("你的生日？（MM-DD，跳过回车）> ").strip() or "未知"
    cfg = {
        "user_name": user_name,
        "user_birthday": user_birthday,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "subtitle": True,
    }
    save_config(cfg)
    print(f"\n好。记住了，{user_name}。\n")
    return cfg


if __name__ == "__main__":
    main()