from datetime import timedelta
import pandas as pd
from binance.client import Client

client = Client()
pd.set_option('display.max_columns',None)

def gettimeedata(symbol, lookback,timeframe, UTC_plus): # Use this as default
    # 參數:幣種{BTCUSDT}(str),現在開始回放幾天{200}(str),時間框架{15m 1h}(st`r)
    # params:
    # days: How many days do u need to grab, time:(str).
    # timeframe: Which timeframe do you need, ex:15m 1h, type:(str).
    # coin: Which pair, ex: BTCUSDT, type:str.
    # UTC_plus: Which time zone you're in, UTC+2 ? UTC+3 ? type:(int) ex:8,-5.
    frame = pd.DataFrame(client.get_historical_klines(symbol,timeframe,lookback+'days ago UTC'))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time', 'open', 'high', 'low', 'close','volume']
    frame.Time = pd.to_datetime(frame.Time, unit='ms')+timedelta(hours=UTC_plus)
    return frame # the output is DataFrame
    # Use function: Dataframe.to_csv('C:/..') to save your file by importing pandas.
