import json

import pandas as pd
import re
import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime

# plt.style.use('fivethirtyeight')
#
# test_data = pd.read_csv("C:\\Users\\justin\\Desktop\\data\\coinbase_eth\\coinbase_ETH_df2h.csv")
# test_data = test_data[['Time', 'open', 'high', 'low', 'close', 'volume']]
#
# test_data['Time'] = pd.to_datetime(test_data['Time'])
# test_data.set_index(pd.DatetimeIndex(test_data['Time'].values))
#
# test_data['close'].plot(figsize=(12.2,6.4))
# plt.title('close bar')
# check_data = pd.read_csv("D:\\downloads\\output_recordcb-2022-11-21_15-43-52.json")
# df = pd.json_normalize(check_data['strategy'])
# df = pd.json_normalize(df['justinstrategy'])
# print(df)
# check_data.to_csv("C:\\Users\\justin\\Desktop\\trade_record.csv")


pattern = re.compile(r'.+\.csv')
paththefile = []
for root, dirs, files in os.walk(r"C:\\Users\\justin\\Desktop\\data\\binance_eth\\"):
    for name in files:
        file_path = os.path.join(root, name)  # 包含路徑的檔案
        if pattern.search(file_path) is not None:
            # print(file_path)#匹配到的檔案 檔案路徑名
            paththefile.append(file_path)



def tojson(file_path):
    dtframe = pd.DataFrame(pd.read_csv(file_path))
    dtframe['Time'] = pd.to_datetime(dtframe['Time'])
    # dtframe.set_index(pd.DatetimeIndex(dtframe['Time'].values))
    new_path = file_path[:-3] + 'json'
    dtframe.to_json(new_path, orient='values')


for i in paththefile:
    tojson(i)



def EMA(data, Time_period, column_name):
    EMA = data[column_name].ewm(span=Time_period, adjust=False).mean()

    return EMA


def DEMA(data, Time_period, column_name):
    ema = EMA(data,Time_period,column_name)
    DEMA = 2*ema - ema.ewm(span=Time_period, adjust=False).mean()

    return DEMA


def tr(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])

    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr


def atr(data, period):
    data['tr'] = tr(data)
    atr = data['tr'].rolling(period).mean()

    return atr


def supertrend(df, period=43, atr_multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]

    return df

def TD9(df):
    close_np = [i for i in df['close']]
    close_shift = np.full_like(close_np, np.nan)
    close_shift[:4] = 0
    close_shift[4:] = close_np[:-4]
    compare_array = close_np > close_shift
    result = np.empty(len(close_np), int)
    counting_number: int = 0
    for i in range(len(close_np)):
        if np.isnan(close_shift[i]):
            result[i] = 0
        else:
            compare_bool = compare_array[i]
            if compare_bool:
                if counting_number >= 0:
                    counting_number += 1
                else:
                    counting_number = 1
            else:
                if counting_number <= 0:
                    counting_number -= 1
                else:
                    counting_number = -1
            result[i] = counting_number
    df['td9'] = pd.DataFrame(result)
    return df


def TD(klinedata):
    close_np = [i["close"] for i in klinedata]
    close_shift = np.empty_like(close_np)
    close_shift[:4] = 0
    close_shift[4:] = close_np[:-4]
    compare_array = close_np > close_shift
    result = np.empty(len(close_np), int)
    counting_number: int = 0
    for i in range(len(close_np)):
        if np.isnan(close_shift[i]):
            result[i] = 0
        else:
            compare_bool = compare_array[i]
            if compare_bool:
                if counting_number >= 0:
                    counting_number += 1
                else:
                    counting_number = 1
            else:
                if counting_number <= 0:
                    counting_number -= 1
                else:
                    counting_number = -1
            result[i] = counting_number
    return result[-5:]


