import sys
from notifier import notify_discord

def run_test():
    # 実際の相場に関係なく、デザインを確認するためのダミーデータ
    dummy_candidates = [
        {
            "symbol": "7203.T",
            "name": "テスト銘柄A (TSE)",
            "current_price": 3500.5,
            "change_rate": 0.045,  # +4.5%
            "change_5min": 0.015,  # +1.5%
            "volume_ratio": 2.5    # 2.5倍
        },
        {
            "symbol": "9984.T",
            "name": "テスト銘柄B (TSE)",
            "current_price": 8600.0,
            "change_rate": 0.031,  # +3.1%
            "change_5min": 0.011,  # +1.1%
            "volume_ratio": 3.1    # 3.1倍
        }
    ]
    
    print("Discordへテスト通知を送信しています...")
    try:
        notify_discord(dummy_candidates)
        print("\n送信が完了しました！Discordの該当チャンネルを確認してください。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    run_test()
