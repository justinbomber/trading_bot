import plotly.graph_objs as go

from datetime import datetime
import pandas_datareader.data as web

df = web.DataReader('AAPL.US', 'quandl',
                    datetime(2007, 10, 1),
                    datetime(2009, 4, 1))

# Make sure dates are in ascending order
# We need this for slicing in the callback below
df.sort_index(ascending=True, inplace=True)

trace = go.Scatter(x=list(df.index),
                   y=list(df.High))

data = [trace]
layout = dict(
    title='Time series with range slider and selectors',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                    label='YTD',
                    step='year',
                    stepmode='todate'),
                dict(count=1,
                    label='1y',
                    step='year',
                    stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = go.FigureWidget(data=data, layout=layout)

