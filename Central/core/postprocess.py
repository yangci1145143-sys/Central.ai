import re

BAD_PATTERNS = [
    r"对不起.{0,20}", r"很抱歉.{0,20}", r"不好意思.{0,20}",
    r"有什么我可以帮", r"很高兴为您", r"希望.{0,10}回答",
    r"如果你有.{0,10}问题", r"作为AI", r"作为一个AI",
    r"你呢[？?]?\s*$", r"请问", r"您好",
    r"谢谢你.{0,10}理解",
]
WENQING_PATTERNS = [
    r"星[光星]", r"月[光亮]", r"光[线芒]", r"如诗", r"如画",
    r"流淌", r"静静地", r"悄悄地", r"轻轻地",
    r"漫过", r"荡漾", r"涟漪", r"余晖", r"斑驳", r"氤氲",
]

def postprocess(text: str) -> str:
    for p in BAD_PATTERNS:
        text = re.sub(p, "", text)
    for p in WENQING_PATTERNS:
        text = re.sub(p, "", text)
    text = re.sub(r"[。，]{2,}", "。", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = text.strip()
    return text if text else "嗯。"