import config

def screen_stocks(market_data):
    """
    取得した株価データに対してスクリーニング条件を適用する。
    条件:
      1. 前日比 +3%以上
      2. 出来高 前日総出来高比で2倍以上
      3. 直近5分で +1%以上
    """
    candidates = []
    
    if not market_data:
        return candidates
        
    for sym, data in market_data.items():
        try:
            prev_close = data["prev_close"]
            current_price = data["current_price"]
            prev_volume = data["prev_volume"]
            current_volume = data["current_volume"]
            price_5min_ago = data["price_5min_ago"]
            
            # ゼロ除算回避
            if prev_close <= 0 or prev_volume <= 0 or price_5min_ago <= 0:
                continue
                
            # 各種比率の計算
            change_rate = (current_price - prev_close) / prev_close
            volume_ratio = current_volume / prev_volume
            change_5min = (current_price - price_5min_ago) / price_5min_ago
            
            # 条件判定
            if (change_rate >= config.MIN_DAILY_CHANGE_RATE and
                volume_ratio >= config.MIN_VOLUME_RATIO and
                change_5min >= config.MIN_5MIN_CHANGE_RATE):
                
                candidate = {
                    **data,
                    "change_rate": change_rate,
                    "volume_ratio": volume_ratio,
                    "change_5min": change_5min
                }
                candidates.append(candidate)
                
        except Exception as e:
            print(f"Error screening {sym}: {e}")
            continue
            
    # 上昇率（前日比）で降順ソート
    sorted_list = sorted(candidates, key=lambda x: x["change_rate"], reverse=True)
    return sorted_list
