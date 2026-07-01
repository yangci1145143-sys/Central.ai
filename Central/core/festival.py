FESTIVALS = {
    "12-25": "圣诞节…大家都在过节呢。",
    "10-31": "万圣节。鬼怪什么的…才不怕。",
    "01-01": "新年。又是新的一年了。",
    "06-15": "…今天是父亲节。",
    "01-16": "…今天是我的生日。",
}

def get_festival(today: str) -> str:
    return FESTIVALS.get(today, "")