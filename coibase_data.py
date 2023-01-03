import requests
from tqdm import tqdm
import pandas as pd
from datetime import datetime, timedelta
import time # 引入time
timeString = "2022-10-25 00:00:00" # 時間格式為字串 從UTC+0的這個時間開始
timeString = datetime.strptime(timeString, '%Y-%m-%d %H:%M:%S')


def get_data(timeframe, coin, deltaday, step):
    apiUrl = 'https://api.pro.coinbase.com'
    sym = coin #'BTC-USD'
    barSize = timeframe #秒
    timeEnd = timeString - timedelta(days=deltaday) - timedelta(seconds=1)
    timeStart = timeEnd - timedelta(days=step) + timedelta(seconds=1)
    timeStart = timeStart.isoformat()
    timeEnd = timeEnd.isoformat()
    # ------------------------ #
    # 獲取網頁返回的json
    parameters = {
        'start':timeStart,
        'end':timeEnd,
        'granularity':barSize
    }
    data = requests.get(f'{apiUrl}/products/{sym}/candles',params=parameters,
                        headers={'content-type':'application/json'})
    # ------------------------- #
    df = pd.DataFrame(data.json(),columns=['Time','low','high','open','close','volume'])
    df['Time'] = pd.to_datetime(df['Time'], unit='s') + timedelta(hours=8) # 時間改爲UTC+8
    return df


def spyder_data(days, timeframe, coin): # 函數引用用這個就好了 上面的不要用
    # 參數為：總共取幾天(int),時間-秒(int),幣種-{BTC-USD}(str)
    btc_list = []
    step = 300/(86400/timeframe)
    timeframe = str(timeframe)
    for i in tqdm(range(0, days, step)):
        btc_df = get_data(timeframe, coin, i, step)
        btc_list.append(btc_df)
    pd.concat(btc_list)
    result = pd.concat(btc_list)
    return result # 數據類型為dataframe
    # 保存公式為 Dataframe.to_csv('C:/..')