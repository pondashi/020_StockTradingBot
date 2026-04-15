import yfinance as yf
import pandas as pd
from datetime import datetime
import time

def fetch_data(symbols):
    """
    指定された銘柄リストのデータを yfinance から取得し、
    スクリーニングに必要な指標を計算できる形式にして返す。
    returns: dict of symbol -> {
        "current_price": float,
        "prev_close": float,
        "current_volume": int,
        "prev_volume": int,
        "price_5min_ago": float,
        "name": str
    }
    """
    try:
        # 日足データ（前日終値、前日出来高の取得用）
        # yfinanceでは最新の日足も含まれるため、period="5d"で取得して直近の確定値を前日とする
        daily_data = yf.download(symbols, period="5d", interval="1d", group_by='ticker', auto_adjust=False, prepost=False, threads=True)
        
        # 5分足データ（現在値、5分前価格、当日出来高の取得用）
        intra_data = yf.download(symbols, period="5d", interval="5m", group_by='ticker', auto_adjust=False, prepost=False, threads=True)
        
        results = {}
        
        # symbolsが1つの場合と複数の場合でpandasのMultiIndex構造が変わるため、統一的に処理
        is_single = len(symbols) == 1
        
        for sym in symbols:
            try:
                # データの抽出
                if is_single:
                    df_daily = daily_data.copy()
                    df_intra = intra_data.copy()
                else:
                    df_daily = daily_data[sym].copy()
                    df_intra = intra_data[sym].copy()
                
                df_daily = df_daily.dropna()
                df_intra = df_intra.dropna()
                
                if len(df_daily) < 2 or len(df_intra) < 2:
                    continue
                
                # 日足データから前日情報（prev_close, prev_volume）を取得
                # [ -2 ] を前日とする（未完了の当日足が [-1] となるケースを考慮）
                # 完全に確定した前日データが欲しい場合は日付比較が必要だが、簡易的に直近から2番目を前日とみなす
                prev_daily = df_daily.iloc[-2]
                prev_close = float(prev_daily['Close'])
                prev_volume = float(prev_daily['Volume'])
                
                # 5分足データから直近の情報（current_price, price_5min_ago, current_volume）を取得
                last_intra = df_intra.iloc[-1]
                prev_intra = df_intra.iloc[-2] # 5分前
                
                current_price = float(last_intra['Close'])
                price_5min_ago = float(prev_intra['Close'])
                
                # yfinanceの5分足の今日のデータを合計して current_volume を算出
                today_str = last_intra.name.strftime('%Y-%m-%d')
                today_intra = df_intra.loc[today_str]
                current_volume = float(today_intra['Volume'].sum())
                
                # 銘柄情報の取得 (Ticker.infoは重いため、シンボル名から簡易的に表示名を作成)
                # 注: 毎回 Ticker(sym).info を呼ぶとAPI制限・パフォ劣化に繋がるため省略
                name = sym.replace('.T', '') + " (TSE)"
                
                results[sym] = {
                    "symbol": sym,
                    "name": name,
                    "current_price": current_price,
                    "prev_close": prev_close,
                    "current_volume": current_volume,
                    "prev_volume": prev_volume,
                    "price_5min_ago": price_5min_ago
                }
            except Exception as e:
                # 特定の銘柄でエラーが発生した場合はスキップ
                print(f"[{sym}] Data extraction error: {e}")
                continue
                
        return results
        
    except Exception as e:
        print(f"API Fetch Error: {e}")
        return None
