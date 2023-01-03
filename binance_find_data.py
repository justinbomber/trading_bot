from datetime import timedelta
import pandas as pd
from binance.client import Client




client = Client()
pd.set_option('display.max_columns',None)

def gettimeedata(symbol, lookback,timeframe): # 函數引用用這個
    # 參數:幣種{BTCUSDT}(str),現在開始回放幾天{200}(str),時間框架{15m 1h}(str)
    frame = pd.DataFrame(client.get_historical_klines(symbol,timeframe,lookback+'days ago UTC'))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time', 'open', 'high', 'low', 'close','volume']
    frame.Time = pd.to_datetime(frame.Time, unit='ms')+timedelta(hours=8)
    return frame # 數據類型為dataframe
    # 保存公式為 Dataframe.to_csv('C:/..')
