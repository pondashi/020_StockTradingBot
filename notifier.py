import requests
from datetime import datetime
import config

def notify_discord(candidates):
    """
    抽出された銘柄リストをDiscord Webhookに通知する。
    """
    if not candidates:
        return
        
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    message_lines = [f"**【急騰銘柄検出】** {now_str}\n"]
    
    for i, cand in enumerate(candidates, 1):
        name = cand["name"]
        symbol = cand["symbol"].replace('.T', '')  # .Tを外して表示
        price = cand["current_price"]
        change_rate = cand["change_rate"] * 100
        change_5min = cand["change_5min"] * 100
        volume_ratio = cand["volume_ratio"]
        
        line = (
            f"**{i}位: {name} ({symbol})**\n"
            f"現在値: {price:,.1f}円\n"
            f"前日比: +{change_rate:.1f}%\n"
            f"5分上昇率: +{change_5min:.1f}%\n"
            f"出来高(前日比): {volume_ratio:.1f}倍\n"
        )
        message_lines.append(line)
        
    payload = {
        "content": "\n".join(message_lines)
    }
    
    try:
        response = requests.post(config.DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print(f"[{now_str}] Discord notification sent successfully. ({len(candidates)} stocks)")
    except requests.exceptions.RequestException as e:
        print(f"[{now_str}] Failed to send Discord notification: {e}")
