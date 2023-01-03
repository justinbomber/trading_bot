import requests
from tqdm import tqdm
import pandas as pd
from datetime import datetime, timedelta
timeString = "2022-10-25 00:00:00" # Time type is String, Begins at UTC+0.
timeString = datetime.strptime(timeString, '%Y-%m-%d %H:%M:%S')

def get_data(timeframe, coin, deltaday, step, UTC_plus):
    apiUrl = 'https://api.pro.coinbase.com'
    sym = coin #'BTC-USD'
    barSize = timeframe #sec
    timeEnd = timeString - timedelta(days=deltaday) - timedelta(seconds=1)
    timeStart = timeEnd - timedelta(days=step) + timedelta(seconds=1)
    timeStart = timeStart.isoformat()
    timeEnd = timeEnd.isoformat()
    # ------------------------ #
    # get the json file from web
    parameters = {
        'start':timeStart,
        'end':timeEnd,
        'granularity':barSize
    }
    data = requests.get(f'{apiUrl}/products/{sym}/candles',params=parameters,
                        headers={'content-type':'application/json'})
    # ------------------------- #
    df = pd.DataFrame(data.json(),columns=['Time','low','high','open','close','volume'])
    df['Time'] = pd.to_datetime(df['Time'], unit='s') + timedelta(hours=UTC_plus) # change the timeframe to UTC+8
    return df


def spyder_data(days, timeframe, coin, UTC_plus): # Use this func to grab the data from coinbase, default.
    # params:
    # days: How many days do u need to grab, 300 days is the maximum, time:(int).
    # timeframe: Which timeframe do you need, !!THE UNIT IS SECOND(S), BE AWARE!!, type:(int).
    # timeframe: Only available in 15m(900), 2h(7200), 4h(14400)
    # coin: Which pair, ex: BTC-USD, type:str.
    # UTC_plus: Which time zone you're in, UTC+2 ? UTC+3 ? type:(int) ex:8,-5.
    btc_list = []
    step = 300/(86400/timeframe)
    timeframe = str(timeframe)
    for i in tqdm(range(0, days, step)):
        btc_df = get_data(timeframe, coin, i, step, UTC_plus)
        btc_list.append(btc_df)
    pd.concat(btc_list)
    result = pd.concat(btc_list)
    return result # the output is DataFrame
    # Use function: Dataframe.to_csv('C:/..') to save your file by importing pandas.

