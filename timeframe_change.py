import pandas as pd
from datetime import datetime

# this transfer_timeframe can convert an timeframe to another
def transfer_timeframe(timefrm,timename,coin):
    cb15m_df = pd.read_csv('C:\\Users\\justin\\Desktop\\data\\coinbase_ETH_df15m.csv')
    cb15m_df = cb15m_df[['Time', 'open', 'high', 'low', 'close', 'volume']]
    cb15m_df['Time'] = cb15m_df['Time'].apply(lambda x: datetime.strptime(x,'%Y/%m/%d %H:%M'))
    cb15m_df = cb15m_df.resample(timefrm, on='Time').agg(
        {
            'open':'first',
            'high':'max',
            'low':'min',
            'close':'last',
            'volume':'sum'
        }
    )
    print(cb15m_df)
    cb15m_df.to_csv(f'C:\\Users\\justin\\Desktop\\data\\coinbase_{coin}_df{timename}.csv')

cb15m_df = pd.read_csv('C:\\Users\\justin\\Desktop\\data\\coinbase_eth\\coinbase_ETH_df15m.csv')
cb15m_df = cb15m_df[['Time', 'open', 'high', 'low', 'close', 'volume']]
cb15m_df['Time'] = cb15m_df['Time'].apply(lambda x: datetime.strptime(x,'%Y/%m/%d %H:%M'))
cb2h = cb15m_df.resample('2h', on='Time').agg(
    {
        'open':'first',
        'high':'max',
        'low':'min',
        'close':'last',
        'volume':'sum'
    }
)

def EMA(data, Time_period):
    EMA = data['close'].ewm(span=Time_period, adjust=False).mean()

    return EMA


def DEMA(data, Time_period):
    ema = EMA(data,Time_period)
    DEMA = 2*ema - ema.ewm(span=Time_period, adjust=False).mean()

    return DEMA

def awesomefunc(df, timeperiod, timeframe):
    cb15m_df = df
    cb15m_df = cb15m_df[['Time', 'open', 'high', 'low', 'close', 'volume']]
    cb15m_df['Time'] = cb15m_df['Time'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d %H:%M'))
    cb2h = cb15m_df.resample(timeframe, on='Time').agg(
        {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }
    )
    cb2h['DEMA'] = DEMA(cb2h, timeperiod)
    aa = cb2h['DEMA']
    bb = cb15m_df.set_index('Time')
    result = bb.join(aa, how='outer')
    result = result.fillna(method='ffill')
    return result['DEMA']

