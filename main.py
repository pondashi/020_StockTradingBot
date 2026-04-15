import schedule
import time
from datetime import datetime
import config
from fetcher import fetch_data
from screener import screen_stocks
from notifier import notify_discord

def is_weekday():
    """現在が平日（月〜金）かどうかを判定する"""
    return datetime.now().weekday() < 5

def job():
    # 土日の場合はスキップ（ログも出さない）
    if not is_weekday():
        return
        
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 定期実行ジョブ開始...")

    # リトライ処理用ループ
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print("1. データ取得中...")
            market_data = fetch_data(config.TARGET_SYMBOLS)
            
            if not market_data:
                raise ValueError("データの取得に失敗しました。")
                
            print(f"2. {len(market_data)} 銘柄のスキャン中...")
            candidates = screen_stocks(market_data)
            
            if candidates:
                print(f"3. 条件を満たす銘柄が見つかりました ({len(candidates)}件)。Discordへ通知します。")
                notify_discord(candidates)
            else:
                print("3. 条件を満たす急騰銘柄はありませんでした。")
                
            break  # 成功したらループを抜ける
            
        except Exception as e:
            print(f"実行中にエラーが発生しました (試行回数 {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print("10秒待機してリトライします...")
                time.sleep(10)
            else:
                print("最大リトライ回数に達しました。次回のスケジュールまで処理をスキップします。")

if __name__ == "__main__":
    print(f"急騰スクリーニングBOT 起動完了")
    print("動作時間: 平日 9:00〜11:30 (9:00-9:30は5分おき、以降は10分おき)")
    print(f"監視対象銘柄数: {len(config.TARGET_SYMBOLS)}")
    
    # 指定された時刻ごとにスケジュールを登録
    for run_time in config.RUN_TIMES:
        schedule.every().day.at(run_time).do(job)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBOTを終了します。")
