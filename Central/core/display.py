# core/display.py

import shutil




def char_width(ch: str) -> int:
    cp = ord(ch)

    if (
        0x4E00 <= cp <= 0x9FFF or
        0x3400 <= cp <= 0x4DBF or
        0x3000 <= cp <= 0x303F or
        0xFF00 <= cp <= 0xFFEF or
        0x2E80 <= cp <= 0x2EFF or
        0xF900 <= cp <= 0xFAFF
    ):
        return 2

    return 1


def text_width(text: str):
    return sum(char_width(c) for c in text)




def get_box_width():

    try:
        cols = shutil.get_terminal_size().columns
    except:
        cols = 80

    cols = max(cols, 60)

    return min(cols - 4, 72)




def wrap_text(text: str, width: int):

    result = []

    current = ""
    current_width = 0

    for ch in text:

        
        if ch == "\n":
            result.append(current)
            current = ""
            current_width = 0
            continue

        w = char_width(ch)

        if current_width + w > width:
            result.append(current)
            current = ch
            current_width = w
        else:
            current += ch
            current_width += w

    if current:
        result.append(current)

    if not result:
        result.append("")

    return result



def show_subtitle(
    text: str,
    speaker: str = "Central",
    mood: str = ""
):

    BOX_WIDTH = get_box_width()

    INNER = BOX_WIDTH - 2

    title = speaker

    if mood:
        title += f"   {mood}"

    print()

    print("┌" + "─" * INNER + "┐")

    pad = INNER - text_width(title)

    print("│" + title + " " * pad + "│")

    print("├" + "─" * INNER + "┤")

    wrapped = wrap_text(text, INNER - 2)

    for line in wrapped:

        line = " " + line

        pad = INNER - text_width(line)

        print("│" + line + " " * pad + "│")

    print("└" + "─" * INNER + "┘")

    print()